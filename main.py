# Standard imports
import argparse
import asyncio
import signal

# Internal imports
from ricardoinfluxrelay.configuration import Configuration


async def main(args):
    # Load configuration
    configuration = Configuration.load_yaml(args.config)

    # Build sockets
    sockets = configuration.build_sockets()

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
        # TODO: find fix for correctly stopping a socket.io client if it is disconnected and re-trying to connect
        # NOTE: Socket.io ignores "asyncio.CancelledError" in "_handle_reconnect"

        # Spawn socket disconnection tasks
        disconnections = [socket.disconnect() for socket in sockets]

        # Await socket disconnections
        await asyncio.gather(*disconnections)


async def exit(signal: signal.Signals, loop: asyncio.AbstractEventLoop) -> None:
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
    parser.add_argument("--config", type=str, required=True, help="Configuration filepath")
    args = parser.parse_args()

    # Get main event loop
    loop = asyncio.get_event_loop()

    # Add signal handlers
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig,
            lambda sig=sig: asyncio.create_task(exit(sig, loop)),
        )

    # Create main task
    mainTask = loop.create_task(main(args))

    try:
        # Execute task loop
        loop.run_forever()
    finally:
        # Close task loop
        loop.close()
