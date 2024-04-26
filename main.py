# Standard imports
import argparse
import asyncio
import signal
import sys

# Internal imports
from ricardoinfluxrelay.configuration import Configuration


async def main(args):
    # Load configuration
    configuration = Configuration.load_yaml(args.config)

    # Build sockets
    sockets = configuration.build_sockets()

    # Spawn socket connection tasks
    connections = [socket.connect() for socket in sockets]

    # Await socket connections
    await asyncio.gather(*connections)

    # Keep relay alive
    while True:
        await sockets[0].client.sleep(1)


def exitHandler(*args, **kwargs):
    # Exit process
    sys.exit()


if __name__ == "__main__":
    # Set signal handlers
    signal.signal(signal.SIGINT, exitHandler)
    signal.signal(signal.SIGTERM, exitHandler)

    # Create argument parser
    parser = argparse.ArgumentParser(prog="Ricardo-InfluxRelay")
    parser.add_argument("--config", type=str, required=True, help="Configuration filepath")
    args = parser.parse_args()

    # Get main event loop
    loop = asyncio.get_event_loop()

    # Execute main function
    loop.run_until_complete(main(args))

    # Exit loop
    loop.close()
