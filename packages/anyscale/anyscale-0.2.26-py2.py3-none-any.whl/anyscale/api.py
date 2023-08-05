import os

import anyscale.util


def report(message: str) -> None:
    """Show a message in the Anyscale Dashboard."""

    session_command_id = os.environ.get("ANYSCALE_SESSION_COMMAND_ID")

    if not session_command_id:
        raise RuntimeError(
            "Trying to use anyscale.report in a command " "not started by anyscale"
        )

    anyscale.util.send_json_request(
        "/api/v2/session_commands/{session_command_id}/report_command".format(
            session_command_id=int(session_command_id)
        ),
        {"message": message},
        method="POST",
    )
