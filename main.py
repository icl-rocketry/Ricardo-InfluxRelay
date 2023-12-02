# Standard imports
import argparse
import asyncio
import datetime
import json
from typing import List, Dict

# Third-party imports
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
from socketio import AsyncClient
import yaml


class Handler:
    def __init__(self, namespace: str, *args, **kwargs) -> None:
        # Store namespace
        self.namespace = namespace

    async def on_event(self, sid: str, data: str) -> None:
        # Throw error if not implemented
        raise NotImplementedError


class MixedHandler(Handler):
    def __init__(self, handlers: List[Handler], *args, **kwargs) -> None:
        # Extract namespaces
        namespaces = [handler.namespace for handler in handlers]

        # Ensure single common namespace
        if len(set(namespaces)) != 1:
            raise ValueError("Non-singular namespaces")

        # Store handlers
        self.handlers = handlers

        # Initialise parent
        super().__init__(namespaces[0])

    async def on_event(self, sid: str, data: str) -> None:
        # Spawn handler tasks
        tasks = [handler.on_event(sid, data) for handler in self.handlers]

        # Wait for tasks to complete
        await asyncio.gather(*tasks)


class PrintHandler(Handler):
    def __init__(self, namespace: str, *args, **kwargs) -> None:
        # Initialise parent
        super().__init__(namespace, *args, **kwargs)

    async def on_event(self, sid: str, data: str) -> None:
        # Print session ID and data
        print(sid, data)


class InfluxDBHandler(Handler):
    def __init__(
        self,
        namespace: str,
        url: str,
        token: str,
        org: str,
        bucket: str,
        tags: Dict[str, str],
        *args,
        **kwargs
    ):
        # Initialise parent
        super().__init__(namespace, *args, **kwargs)

        # Declare InfluxDB client
        self.client = InfluxDBClient(url=url, token=token, org=org)

        # Set bucket name by stripping leading forward slash
        self.bucket = bucket

        # Set tags
        self.tags = tags

        # Create write API
        self.write_api = self.client.write_api(write_options=ASYNCHRONOUS)

    async def on_event(self, sid: str, data: str) -> None:
        # Construct current time in ISO format
        # TODO: use backend/system time?
        time = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # Convert data string to dictionary
        data_ = json.loads(data)

        # Create InfluxDB point
        point = Point.from_dict(
            {
                "time": time,
                "measurement": sid,
                "tags": self.tags,
                "fields": data_,
            }
        )

        # Write point
        self.write_api.write(bucket=self.bucket, record=point)


# Handler mapping
handlerMapping = {"print": PrintHandler, "influxdb": InfluxDBHandler}


class SocketRelay:
    def __init__(self, handlers: List[Handler]):
        # Declare socketio client
        self.client = AsyncClient()

        # Extract namespaces
        namespaces = [handler.namespace for handler in handlers]

        # Check for repeated namespaces
        if len(set(namespaces)) != len(namespaces):
            raise ValueError("Repeated namespaces in handlers")

        # Iterate through handlers
        for handler in handlers:
            # Register handler
            self.client.on(
                event="*",
                namespace=handler.namespace,
                handler=handler.on_event,
            )

    async def connect(self, url: str) -> None:
        # Connect client
        await self.client.connect(url)

    async def disconnect(self) -> None:
        # Disconnect client
        await self.client.disconnect()


async def main(args):
    # Load config
    # TODO: environment variable handling (https://pypi.org/project/envyaml/)?
    with open(args.config, "r") as fid:
        config = yaml.load(fid, Loader=yaml.CSafeLoader)

    # Validate config
    # TODO: implement

    # Extract handlers from configuration
    configHandlers = config["handlers"]

    # Declare list of handlers
    handlers = {}

    # Iterate through handlers
    for handler in configHandlers:
        # Extract handler type and namespace
        type = handler["type"]
        namespace = handler["namespace"]

        # Extract class from handler mapping
        handlerType = handlerMapping[type]

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


if __name__ == "__main__":
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
