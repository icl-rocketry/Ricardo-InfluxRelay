# Standard imports
import argparse
import logging
import signal

# Internal imports
from ricardoinfluxrelay.relay import Relay

# Set logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - PID%(process)d - %(levelname)s - %(message)s",
)


def main(args) -> None:
    # Create relay
    relay = Relay.load_yaml(args.config)

    # Declare exit handler
    def exit_handler(signum, frame) -> None:
        # Shutdown relay
        relay.shutdown()

    # Add signal handlers
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, exit_handler)

    # Run relay
    relay.run()


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

    # Execute relay
    main(args)
