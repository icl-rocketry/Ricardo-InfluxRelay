# Standard imports
import json
from typing import Dict

# Third-party imports
import flatten_json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Internal imports
from .handler import Handler


class InfluxDBHandler(Handler):
    def __init__(
        self,
        namespace: str,
        url: str,
        org: str = "",
        bucket: str = "",
        tags: Dict[str, str] = {},
        token: str = "",
    ):
        # Initialise parent
        super().__init__(namespace, tags)

        # Declare InfluxDB client
        self.client = InfluxDBClient(url=url, token=token, org=org)

        # Set bucket name
        self.bucket = bucket

        # Create write API
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    async def on_event(
        self,
        event: str,
        data: str,
        extra_tags: Dict[str, str] = {},
    ) -> None:
        # Generate tags
        tags = {**self.tags, **extra_tags}

        # Convert data string to dictionary
        packet = json.loads(data)

        # Extract timestamp (in nano-seconds)
        timestamp = int(packet["timestamp"] * 1e6)

        # Flatten data dictionary
        data_flat = flatten_json.flatten(packet["data"], separator=".")

        # TODO: check types?

        # Create InfluxDB point
        point = Point.from_dict(
            {
                "time": timestamp,
                "measurement": event,
                "tags": tags,
                "fields": data_flat,
            }
        )

        # Write point
        self.write_api.write(
            bucket=self.bucket,
            record=point,
            write_precision=WritePrecision.NS,
        )
