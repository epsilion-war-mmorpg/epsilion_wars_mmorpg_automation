"""TData to session-file converter."""

import argparse
import asyncio

from opentele.api import UseCurrentSession
from opentele.td import TDesktop


async def main(tdata_filepath: str) -> None:
    """Get tdata from selected path and generate .session file."""
    tdesk = TDesktop(tdata_filepath)
    if not tdesk.isLoaded():
        raise RuntimeError('tdata not loaded!')

    client = await tdesk.ToTelethon(
        session='.epsilion_automation_session_converted.session',
        flag=UseCurrentSession,
    )
    await client.connect()
    await client.PrintSessions()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert tdata to .session file.',
    )
    parser.add_argument(
        '-f',
        '--filepath',
        dest='filepath',
        required=True,
        type=str,
        help='Path to tdata folder. For example: ~/.local/share/TelegramDesktop/tdata',
    )
    args = parser.parse_args()

    asyncio.run(main(args.filepath))
