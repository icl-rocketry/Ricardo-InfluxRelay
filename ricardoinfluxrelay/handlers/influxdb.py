# Standard imports
import logging
from typing import Dict, List

# Third-party imports
from influxdb_client import InfluxDBClient, WritePrecision

# Internal imports
from .handler import Handler
from ricardoinfluxrelay.event import Event

# TODO: implement QuestDB specific library?


class InfluxDBHandler(Handler):
    def __init__(
        self,
        namespaces: List[str],
        url: str,
        org: str = "",
        bucket: str = "",
        tags: Dict[str, str] = {},
        token: str = "",
        *args,
        **kwargs,
    ):
        # Initialise parent
        super().__init__(namespaces, tags, *args, **kwargs)

        # Store InfluxDB parameters
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket

    def _initialise(self) -> bool:
        # Create InfluxDB client
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)

        # Create write API
        self.write_api = self.client.write_api()

        # Log initialisation
        # TODO: add additional information
        logging.info("InfluxDB handler initialised")

        # Return success
        return True

    def _deinitialise(self) -> None:
        # Log deinitialisation
        # TODO: add additional information
        logging.info("InfluxDB handler deinitialised")

    def _on_event(self, event: Event) -> None:
        # Convert data to point
        point = event.to_point()

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
