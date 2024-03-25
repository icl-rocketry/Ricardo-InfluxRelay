# Standard imports
from datetime import datetime, timezone
import json
from typing import Dict

# Third-party imports
import flatten_json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS

# Internal imports
from .handler import Handler


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
        **kwargs,
    ):
        # Initialise parent
        super().__init__(namespace, *args, **kwargs)

        # Declare InfluxDB client
        self.client = InfluxDBClient(url=url, token=token, org=org)

        # Set bucket name
        self.bucket = bucket

        # Set tags
        self.tags = tags

        # Create write API
        self.write_api = self.client.write_api(write_options=ASYNCHRONOUS)

    async def on_event(self, sid: str, data: str) -> None:
        # Convert data string to dictionary
        packet = json.loads(data)

        # Extract timestamp (in nano-seconds)
        timestamp = int(packet["timestamp"] * 1e6)

        # Flatten data dictionary
        data_flat = flatten_json.flatten(packet["data"])

        # TODO: check types?

        # Create InfluxDB point
        point = Point.from_dict(
            {
                "time": timestamp,
                "measurement": sid,
                "tags": self.tags,
                "fields": data_flat,
            }
        )

        # Write point
        self.write_api.write(
            bucket=self.bucket, record=point, write_precision=WritePrecision.NS
        )
