# Standard imports
import argparse
import asyncio
import signal
import sys
import logging
from typing import List

# Internal imports
from ricardoinfluxrelay.configuration import Configuration
from ricardoinfluxrelay.socketrelay import SocketRelay

# Set logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


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

        # Log disconnections
        logging.info("Sockets disconnected")


async def exit(signal: signal.Signals, loop: asyncio.AbstractEventLoop) -> None:
    # Log exit signal
    logging.info(f"Exit signal ({signal}) received")

    # Get tasks to cancel
    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]

    # Cancel tasks
    [task.cancel() for task in tasks]

    # Wait for tasks to finish
    await asyncio.gather(*tasks, return_exceptions=True)

    # Stop loop
    loop.stop()


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

    # Log configuration load
    logging.info("Configuration loaded")

    # Build sockets
    sockets = configuration.get_sockets()

    # Log socket creation
    logging.info("Sockets created")

    # Get main event loop
    loop = asyncio.get_event_loop()

    # Add signal handlers
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig,
            lambda sig=sig: asyncio.create_task(exit(sig, loop)),
        )

    # Log start
    logging.info("Starting main execution")

    # Create main task
    mainTask = loop.create_task(main(sockets))

    try:
        # Execute task loop
        loop.run_forever()
    finally:
        # Close task loop
        loop.close()
