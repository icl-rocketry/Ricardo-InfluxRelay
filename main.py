# Standard imports
import argparse
import asyncio
import signal
import sys

# Third-party imports
import yaml

# Internal imports
from ricardoinfluxrelay.handlers import MixedHandler, get_handler
from ricardoinfluxrelay.socketrelay import SocketRelay


async def main(args):
    # Load config
    # TODO: environment variable handling (https://pypi.org/project/envyaml/)?
    with open(args.config, "r") as fid:
        config = yaml.load(fid, Loader=yaml.CSafeLoader)

    # Validate config
    # TODO: implement

    # Extract handlers from configuration
    configHandlers = config["handlers"]

    # Declare dictionary of handlers
    handlers = {}

    # Iterate through handlers
    for handler in configHandlers:
        # Extract handler type and namespace
        type = handler["type"]
        namespace = handler["namespace"]

        # Extract class from handler mapping
        handlerType = get_handler(type)

        # Create list if namespace not seen previously
        if namespace not in handlers:
            handlers[namespace] = []

        # Append handler object
        handlers[namespace].append(handlerType(**handler))

    # Group handlers
    groupedHandlers = [MixedHandler(ihandlers) for _, ihandlers in handlers.items()]

    # Create socket relay
    relay = SocketRelay(groupedHandlers)

    # Connect socket relay
    await relay.connect(config["socket"]["url"])

    # Keep relay alive
    while True:
        await relay.client.sleep(1)


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
