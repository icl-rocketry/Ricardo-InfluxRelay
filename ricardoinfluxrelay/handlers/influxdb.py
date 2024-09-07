# Standard imports
from typing import Any, Dict, List

# Third-party imports
from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Internal imports
from .sanitised import SanitisedHandler


class InfluxDBHandler(SanitisedHandler):
    def __init__(
        self,
        namespaces: List[str],
        url: str,
        org: str = "",
        bucket: str = "",
        tags: Dict[str, str] = {},
        token: str = "",
    ):
        # Initialise parent
        super().__init__(namespaces, tags)

        # Declare InfluxDB client
        self.client = InfluxDBClient(url=url, token=token, org=org)

        # Set bucket name
        self.bucket = bucket

        # Create write API
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    async def _on_event(
        self,
        namespace: str,
        event: str,
        data: Dict[str, Any],
        tags: Dict[str, str],
    ) -> None:
        # Convert data to point
        point = self._to_point(event, data, tags)

        # TODO: check types?

        # Write point
        self.write_api.write(
            bucket=self.bucket,
            record=point,
            write_precision=WritePrecision.NS,
        )
