# Standard imports
import json
import os
from typing import Dict, List

# Third-party imports
import flatten_json
from influxdb_client import Point

# Internal imports
from .handler import Handler


class FileHandler(Handler):

    def __init__(self, namespaces: List[str], filepath: str, tags: Dict[str, str] = {}):
        # Initialise parent
        super().__init__(namespaces, tags)

        # Ensure directory exists
        os.makedirs(
            os.path.dirname(os.path.abspath(filepath)),
            exist_ok=True,
        )

        # Open file (append mode)
        self.fid = open(filepath, "a")

    def __del__(self):
        # Close file
        self.fid.close()

    async def _on_event(
        self,
        namespace: str,
        event: str,
        data: str,
        tags: Dict[str, str],
    ) -> None:
        # Convert data string to dictionary
        packet = json.loads(data)

        # Extract timestamp (in nano-seconds)
        timestamp = int(packet["timestamp"] * 1e6)

        # Flatten data dictionary
        data_flat = flatten_json.flatten(packet["data"], separator=".")

        # TODO: check types?
        # TODO: unify point generation with InfluxHandler?

        # Create InfluxDB point
        point = Point.from_dict(
            {
                "time": timestamp,
                "measurement": event,
                "tags": tags,
                "fields": data_flat,
            }
        )

        # Write point to file
        self.fid.write(str(point) + "\n")
