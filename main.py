# Standard imports
import argparse
import asyncio
import signal
import sys
from typing import List

# Internal imports
from ricardoinfluxrelay.configuration import Configuration
from ricardoinfluxrelay.socketrelay import SocketRelay


async def main(sockets: List[SocketRelay]) -> None:

    try:
        # Spawn socket connection tasks
        connect = [socket.connect() for socket in sockets]

        # Await socket connections
        await asyncio.gather(*connect)

        # Spawn socket connected tasks
        connected = [socket.wait() for socket in sockets]

        # Await connection with server to finish
        await asyncio.gather(*connected)

    finally:
        # Spawn socket disconnection tasks
        disconnections = [socket.disconnect() for socket in sockets]

        # Await socket disconnections
        await asyncio.gather(*disconnections)


async def exit(signal: signal.Signals, loop: asyncio.AbstractEventLoop) -> None:
    # Forcibly exit the process
    # TODO: Find fix for correctly stopping Socket.IO clients which are trying to connect
    #       as python-socketio ignores "asyncio.CancelledError" in "_handle_reconnect".
    #       Discussed in: https://github.com/miguelgrinberg/python-socketio/issues/1333.
    sys.exit()

    # # Get tasks to cancel
    # tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]

    # # Cancel tasks
    # [task.cancel() for task in tasks]

    # # Wait for tasks to finish
    # await asyncio.gather(*tasks, return_exceptions=True)

    # # Stop loop
    # loop.stop()


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(prog="Ricardo-InfluxRelay")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Configuration filepath",
    )
    args = parser.parse_args()

    # Load configuration
    configuration = Configuration.load_yaml(args.config)

    # Build sockets
    sockets = configuration.get_sockets()

    # Get main event loop
    loop = asyncio.get_event_loop()

    # Add signal handlers
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig,
            lambda sig=sig: asyncio.create_task(exit(sig, loop)),
        )

    # Create main task
    mainTask = loop.create_task(main(sockets))

    try:
        # Execute task loop
        loop.run_forever()
    finally:
        # Close task loop
        loop.close()
