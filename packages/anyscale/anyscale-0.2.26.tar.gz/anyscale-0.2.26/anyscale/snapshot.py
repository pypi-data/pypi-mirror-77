import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
from subprocess import STDOUT
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple, Union

import click
import ray.ray_constants
import requests

from anyscale.conf import (
    DOCKER_REGISTRY,
    DOCKER_SNAPSHOT_BUCKET,
    REGISTRY_IMAGE,
    SNAPSHOT_REPO,
    SNAPSHOT_REPO_PASSWORD,
)
from anyscale.feature_flags import FLAG_KEY_USE_SNAPSHOT
from anyscale.project import get_project_id
from anyscale.util import (
    check_is_feature_flag_on,
    confirm,
    get_cluster_config,
    get_requirements,
    send_json_request,
    Timer,
)


logging.basicConfig(format=ray.ray_constants.LOGGER_FORMAT)
logger = logging.getLogger(__file__)

REGISTRY_CONF_PATH = "/etc/docker/registry/config.yml"

REGISTRY_CONF_TEMPLATE = """
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  s3:
    accesskey: {ACCESS_KEY}
    secretkey: {SECRET_KEY}
    sessiontoken: {STS_TOKEN}
    region: {REGION}
    bucket: {BUCKET}
    rootdirectory: {S3_PATH}
http:
  addr: :5555
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
"""


class SnapshotRunner:
    def __init__(self, print_snapshot_info: bool = True) -> None:
        self.snapshot_home = os.path.expanduser("~/.anyscale/snapshot")
        self.password = SNAPSHOT_REPO_PASSWORD
        self.snapshot_repo = SNAPSHOT_REPO
        self.print_snapshot_info = print_snapshot_info

        # Get the right restic executable path depending on the OS.
        current_dir = os.path.dirname(os.path.realpath(__file__))
        if sys.platform.startswith("linux"):
            self.snapshot_executable = os.path.join(current_dir, "restic-linux")
        elif sys.platform.startswith("darwin"):
            self.snapshot_executable = os.path.join(current_dir, "restic-darwin")
        else:
            raise NotImplementedError(
                "Restic snapshot not supported on platform {}".format(sys.platform)
            )

    def setup(self) -> None:
        proc = subprocess.Popen(
            [self.snapshot_executable, "init", "-r", self.snapshot_repo],
            env={"RESTIC_PASSWORD": self.password},
        )

        proc.communicate()

    def upload(
        self,
        snapshot_uuid: str,
        project_dir: str,
        additional_files: List[str],
        files_only: bool,
        creds: Dict[str, str],
    ) -> None:
        """This function takes and upload a snapshot to S3. The snapshot
        consists of all the items in project_dir (if specified) and any
        additional_files specified.

        Args:
            snapshot_uuid: uuid of the snapshot to be uploaded to restic repo.
            project_dir: directory of the anyscale project.
            additional_files: additional files to be included with the snapshot (if any).
            creds: credentials used to access S3.
        """
        additional_files_list = tempfile.NamedTemporaryFile()
        with open(additional_files_list.name, "w") as temp:
            for f in additional_files:
                temp.write(f + "\n")

        new_env = os.environ.copy()
        new_env = {**new_env, **creds}
        new_env["RESTIC_PASSWORD"] = self.password
        proc = subprocess.Popen(
            [
                self.snapshot_executable,
                "-r",
                self.snapshot_repo,
                "backup",
                "--files-from",
                additional_files_list.name,
                "" if files_only else project_dir,
                "--tag",
                snapshot_uuid,
                "--tag",
                "project_dir=" + project_dir,
                "--verbose",
                "--verbose",
            ],
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        collecting_output = False
        collected_out = ""
        while True:
            if proc.stdout:
                line = proc.stdout.readline()
                if not line:
                    break

                if b"open repository" in line:
                    timer = Timer("Taking snapshot of all files within this project")
                    timer.start()
                elif b"start backup" in line:
                    timer.stop()
                    timer = Timer("Saving snapshot to Anyscale")
                    timer.start()
                elif b"scan finished" in line:
                    timer.stop()
                    if self.print_snapshot_info:
                        print("\n" + line.decode())
                elif not collecting_output and line == b"\n":
                    collected_out = ""
                    collecting_output = True

                if collecting_output:
                    collected_out += line.decode()
        if self.print_snapshot_info:
            print(collected_out)

    def download(
        self, name: str, target_directory: Union[str, Path], creds: Dict[str, str],
    ) -> None:
        """This function downloads a snapshot from S3 to a target directory.
        The snapshot could be of a project, in which case it will have all
        project files and possibly output_files. Or it could be of any files
        on the remote cluster.
        Args:
            name: id of the snapshot to download.
            target_directory: directory to download the snapshot to.
            creds: credentials used to download the snapshot.
        """
        new_env = os.environ.copy()
        new_env = {**new_env, **creds}
        new_env["RESTIC_PASSWORD"] = self.password

        restic_id, project_dir, additional_files = self.get_restic_info(name, new_env)

        with tempfile.TemporaryDirectory() as snapshot_dir:
            proc = subprocess.Popen(
                [
                    self.snapshot_executable,
                    "-r",
                    self.snapshot_repo,
                    "restore",
                    "--tag",
                    name,
                    "latest",
                    "--target",
                    snapshot_dir,
                ],
                env=new_env,
                stderr=STDOUT,
            )

            proc.communicate()

            # Convert absolute path used by restic to relative path
            # Strip the leading "/"
            relative_directory = project_dir[1:]
            current_dir = os.path.join(snapshot_dir, relative_directory)
            if os.path.exists(current_dir):
                # Copy the src directory to dst directory recursively
                # and overwrite if the file already exists
                proc = subprocess.Popen(["rsync", "-a", current_dir, target_directory])
                proc.communicate()

            # Move additional files
            for additional_file in additional_files:
                proc = subprocess.Popen(
                    [
                        "rsync",
                        "-a",
                        os.path.join(snapshot_dir, additional_file[1:]),
                        target_directory,
                    ]
                )
                proc.communicate()

    def delete(self, name: str, creds: Dict[str, str]) -> None:
        new_env = os.environ.copy()
        new_env = {**new_env, **creds}
        new_env["RESTIC_PASSWORD"] = self.password

        # Getting restic snapshot ID from snapshot_uuid
        # Need this because we cannot delete snapshot with --tag
        restic_id, _, _ = self.get_restic_info(name, new_env)

        # Need this because if a deletion fails, restic repo will be locked.
        proc = subprocess.Popen(
            [self.snapshot_executable, "-r", self.snapshot_repo, "unlock"],
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Actual deletion
        proc = subprocess.Popen(
            [
                self.snapshot_executable,
                "-r",
                self.snapshot_repo,
                "forget",
                restic_id,
                "--prune",
            ],
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = proc.communicate()
        if proc.returncode != 0:
            print(output, error)

    def describe(self, name: str, creds: Dict[str, str]) -> List[Dict[str, str]]:
        new_env = os.environ.copy()
        new_env = {**new_env, **creds}
        new_env["RESTIC_PASSWORD"] = self.password

        restic_id, project_dir, _ = self.get_restic_info(name, new_env)
        proc = subprocess.Popen(
            [
                self.snapshot_executable,
                "-r",
                self.snapshot_repo,
                "ls",
                restic_id,
                "--recursive",
                project_dir,
                "--json",
            ],
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = proc.communicate()
        if proc.returncode != 0:
            print(output, error)

        snapshot_items = []
        for element in output.strip().split(b"\n"):
            snapshot_item = json.loads(element)
            path = snapshot_item.get("path")
            if path == project_dir:
                continue
            if path:
                snapshot_item["path"] = path[len(project_dir) :]
                snapshot_items.append(snapshot_item)

        return snapshot_items

    def get_restic_info(
        self, tag: str, new_env: Dict[str, str]
    ) -> Tuple[str, str, List[str]]:
        # Getting restic snapshot ID from snapshot_uuid
        # Need this because we cannot delete snapshot with --tag
        proc = subprocess.Popen(
            [
                self.snapshot_executable,
                "-r",
                self.snapshot_repo,
                "snapshots",
                "--tag",
                tag,
                "--json",
            ],
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = proc.communicate()
        if proc.returncode != 0:
            print(output, error)

        return parse_restic_snapshots_output(output)


snapshot_runner = SnapshotRunner(
    print_snapshot_info=check_is_feature_flag_on(FLAG_KEY_USE_SNAPSHOT, True)
)


def parse_restic_snapshots_output(output: bytes) -> Tuple[str, str, List[str]]:
    """
    This function takes an ouput from the "restic snapshots" cmd
    and extract restic snapshot id and its project_dir
    """
    snapshots_info = json.loads(output.decode())
    assert snapshots_info and len(snapshots_info) >= 1, "Snapshot not found"
    snapshot_info = snapshots_info[0]
    project_dir_prefix = "project_dir="
    project_dir = ""
    for tag in snapshot_info["tags"]:
        if tag.startswith(project_dir_prefix):
            project_dir = tag[len(project_dir_prefix) :]
    assert (
        len(project_dir) > 0
    ), "Project directory not found. Maybe it's not tagged to the snapshot?"

    output_files = []
    for path in snapshot_info["paths"]:
        if not path.startswith(os.path.abspath(project_dir)):
            output_files.append(path)

    return snapshot_info["short_id"], project_dir, output_files


def copy_file(to_s3: bool, source: str, target: Any, download: bool) -> None:
    """Copy a file.

    The file source or target may be on S3.

    Args:
        to_s3 (bool): If this is True, then copy to/from S3, else the local
            disk. If this is True, then the file source or target will be a
            presigned URL to which GET or POST HTTP requests can be sent.
        source (str or S3 URL): Source file local pathname or S3 GET URL. If
            this is an S3 URL, target is assumed to be a local pathname.
        target (str or S3 URL): Target file local pathname or S3 URL with POST
            credentials. If this is an S3 URL, source is assumed to be a local
            pathname.
        download (bool): If this is True, then this will upload from source to
            target, else this will download.
    """
    try:
        if to_s3:
            if download:
                with open(target, "wb") as f:
                    response = requests.get(source)
                    for block in response.iter_content(1024):
                        f.write(block)
            else:
                with open(source, "rb") as f:
                    files = {"file": ("object", f)}
                    resp = requests.post(
                        target["url"], data=target["fields"], files=files
                    )
                    assert resp.ok, resp.text
        else:
            shutil.copyfile(source, target)
    except (OSError, AssertionError) as e:
        logger.warn("Failed to copy file %s , aborting", source)
        raise e


def create_snapshot(
    project_definition: Any,
    yes: bool,
    description: Optional[str] = None,
    include_output_files: bool = False,
    additional_files: List[str] = [],
    files_only: bool = False,
    tags: List[str] = [],
    run_upload: bool = False,
) -> str:
    """Create a snapshot of a project.

    Args:
        project_definition: Project definition.
        yes: Don't ask for confirmation.
        description: An optional description of the snapshot.
        include_output_files: Whether or not to include output files.
        additional_files: Additional files to include in the snapshot.
        files_only: Only include additional files in the snapshot.
        tags: Tags for the snapshot.
        run_upload: Whether to actually upload the restic snapshot.

    Raises:
        ValueError: If the current project directory does not match the project
            metadata entry in the database.
        Exception: If saving the snapshot files fails.
    """
    # Find and validate the current project ID.
    project_dir = project_definition.root
    project_id = get_project_id(project_dir)

    if include_output_files:
        for output_file in project_definition.config.get("output_files", []):
            if output_file[0] == "/" and not output_file.startswith(project_dir):
                additional_files.append(output_file)

    cluster_config = get_cluster_config(
        os.path.join(project_dir, project_definition.cluster_yaml())
    )

    if "requirements" in project_definition.config.get("environment", {}):
        requirements = get_requirements(
            os.path.join(
                project_dir, project_definition.config["environment"]["requirements"]
            )
        )
    else:
        requirements = ""

    resp = send_json_request(
        "/api/v2/snapshots/",
        {
            "project_id": project_id,
            "project_config": json.dumps(project_definition.config),
            "cluster_config": json.dumps(cluster_config),
            "requirements": requirements,
            "description": description if description else "",
            "tags": tags,
        },
        method="POST",
    )
    snapshot_uuid: str = resp["result"]["id"]

    if check_is_feature_flag_on(FLAG_KEY_USE_SNAPSHOT, True) and run_upload:

        creds = resp["result"]["credentials"]

        try:
            snapshot_runner.upload(
                snapshot_uuid, project_dir, additional_files, files_only, creds
            )
        except (OSError, AssertionError):
            pass

    return snapshot_uuid


def describe_snapshot(uuid: str) -> Any:
    resp = send_json_request("/api/v2/snapshots/{}".format(uuid), {})
    return resp["result"]


def list_snapshots(project_dir: str) -> List[str]:
    """List all snapshots associated with the given project.

    Args:
        project_dir: Project root directory.

    Returns:
        List of Snapshots for the current project.

    Raises:
        ValueError: If the current project directory does not match the project
            metadata entry in the database.
    """
    # Find and validate the current project ID.
    project_id = get_project_id(project_dir)
    resp = send_json_request("/api/v2/snapshots/", {"project_id": project_id})
    snapshots = resp["result"]["snapshots"]
    return [snapshot["id"] for snapshot in snapshots]


def get_snapshot_uuid(project_dir: str, snapshot_uuid: str) -> str:
    """Get a snapshot of the given project with the given name.

    Args:
        project_id: The ID of the project.
        snapshot_name: The name of the snapshot to get. If there are multiple
            snapshots with the same name, then the user will be prompted to
            choose a snapshot.
    """
    # Find and validate the current project ID.
    project_id = get_project_id(project_dir)
    resp = send_json_request("/api/v2/snapshots/", {"project_id": project_id})
    snapshots = resp["result"]["snapshots"]
    if len(snapshots) == 0:
        raise ValueError("No snapshots found with name {}".format(snapshot_uuid))
    snapshot_idx = 0
    if len(snapshots) > 1:
        print(
            "More than one snapshot found with UUID {}. "
            "Which do you want to use?".format(snapshot_uuid)
        )
        for i, snapshot in enumerate(snapshots):
            print("{}. {}".format(i + 1, snapshot["uuid"]))
        snapshot_idx = click.prompt(
            "Please enter a snapshot number from 1 to {}".format(len(snapshots)),
            type=int,
        )
        snapshot_idx -= 1
        if snapshot_idx < 0 or snapshot_idx > len(snapshots):
            raise ValueError("Snapshot index {} is out of range".format(snapshot_idx))
    result: str = snapshots[snapshot_idx]["id"]
    return result


def download_snapshot(
    name: str,
    credentials: Dict[str, str],
    target_directory: Optional[str] = None,
    overwrite: bool = False,
) -> str:
    """Download a snapshot to a local target directory.

    This will recreate the original directory structure of the snapshot. Only
    input files (those found in the project directory during the snapshot
    creation) will be downloaded, not output files specified in the
    project.yaml.

    Args:
        snapshot_info: Information about the snapshot as returned by
            snapshot_get.
        credentials: AWS credentials for accessing S3.
        target_directory: Directory this snapshot gets downloaded to.
            If None, the snapshot will be downloaded to a temporary directory.

    Returns:
        str: The directory where the snapshot has been downloaded to.
    """
    if not target_directory:
        target_directory = os.path.join(os.getcwd(), name)
    target_directory = os.path.abspath(target_directory)
    if os.path.exists(target_directory) and not overwrite:
        print(
            'Target directory already exists. Run with "--overwrite" flag to overwrite the target directory.'
        )
        return ""
    snapshot_runner.download(name, target_directory, credentials)

    return target_directory


def generate_docker_image_name(project_id: int, snapshot_id: str) -> str:
    tag = f"{project_id}_{snapshot_id}"
    return DOCKER_REGISTRY + "/snapshots:" + tag


def restore_docker_snapshot_commands(
    cluster_config: Dict[str, Any],
    project_id: int,
    snapshot_id: str,
    session_id: int,
    directory_name: str,
) -> List[str]:
    new_image_name = generate_docker_image_name(project_id, snapshot_id)
    cluster_config["docker"]["image"] = new_image_name

    docker_mounts = [
        "-v {dst}:/root/backup/file_mounts/{dst}:ro"
        for dst in cluster_config.get("file_mounts", {}).keys()
    ]
    docker_mounts.append(
        f"-v /home/ubuntu/{directory_name}:/root/backup/{directory_name}:ro "
    )

    restore_commands = [
        f"mkdir -p {mount}" for mount in cluster_config.get("file_mounts", {}).keys()
    ]

    restore_commands.append(f"mkdir -p /home/ubuntu/{directory_name}")

    # TODO(ilr) Move away from /root in container.
    restore_commands.extend(
        [
            f"docker run --rm --name temp_backup_{session_id} -d -it -v $HOME/{directory_name}:/root/backup/{directory_name} {new_image_name}-files bash",
            f"docker exec temp_backup_{session_id} rsync -a /root/save_dir/{directory_name} /root/backup/",
            f"docker stop temp_backup_{session_id}",
        ]
    )
    return restore_commands


def restart_registry_commands(user_aws_credentials: Any, project_id: int,) -> List[str]:
    registry_config_content = REGISTRY_CONF_TEMPLATE
    registry_config_content = registry_config_content.format(
        ACCESS_KEY=user_aws_credentials["AWS_ACCESS_KEY_ID"],
        SECRET_KEY=user_aws_credentials["AWS_SECRET_ACCESS_KEY"],
        STS_TOKEN=user_aws_credentials["AWS_SESSION_TOKEN"],
        REGION="us-west-2",  # TODO: revisit for customer accounts.
        BUCKET=DOCKER_SNAPSHOT_BUCKET,  # TODO: revisit for customer accounts.
        S3_PATH=f"docker/{project_id}",
    )

    return [
        f"docker stop registry || true && mkdir -p /tmp/docker/registry/ && cat >/tmp/docker/registry/config.yml <<'EOL'{registry_config_content}\nEOL",
        f"docker run -d -p 5555:5555 -v /tmp/docker/registry/config.yml:{REGISTRY_CONF_PATH} --name registry {REGISTRY_IMAGE}  || docker start registry",
    ]
