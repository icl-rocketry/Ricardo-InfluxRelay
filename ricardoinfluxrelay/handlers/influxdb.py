# Standard imports
import logging
from typing import Any, Dict, List

# Third-party imports
from influxdb_client import InfluxDBClient, WritePrecision

# Internal imports
from .sanitised import SanitisedHandler

# TODO: implement QuestDB specific library?


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

        # Store InfluxDB parameters
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket

    def start(self):
        # Create InfluxDB client
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)

        # Create write API
        self.write_api = self.client.write_api()

    def _on_event(
        self,
        namespace: str,
        event: str,
        data: Dict[str, Any],
        tags: Dict[str, str],
    ) -> None:
        # Convert data to point
        point = self._to_point(event, data, tags)

        # TODO: check types?

        try:
            # Try to write point
            self.write_api.write(
                bucket=self.bucket,
                record=point,
                write_precision=WritePrecision.NS,
            )
        except:
            # Log error
            logging.error(f"Failed to write to {self.url}")
