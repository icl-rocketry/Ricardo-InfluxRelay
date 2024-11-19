# Standard imports
from dataclasses import dataclass
import json
from typing import Any, Dict

# Third-party imports
import flatten_json
from influxdb_client import Point


@dataclass
class Event:
    namespace: str
    event: str
    data: Dict[str, Any]
    tags: Dict[str, str]

    def __init__(
        self,
        namespace: str,
        event: str,
        data: str | Dict[str, Any],
        tags: Dict[str, str],
    ) -> None:
        # TODO: type checks?

        # Store namespace
        self.namespace = namespace

        # Store event
        self.event = event

        # Store data
        if isinstance(data, str):
            self.data = json.loads(data)
        else:
            self.data = data

        # Store tags
        self.tags = tags

    def __str__(self) -> str:
        # Return stringified dictionary representation
        return str(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        # Return dictionary representation
        return {
            "namespace": self.namespace,
            "event": self.event,
            "data": self.data,
            "tags": self.tags,
        }

    def to_point(self) -> Point:
        # Extract timestamp
        timestamp = self.data["timestamp"]
        timestamp_ns = int(timestamp * 1e6)

        # Flatten data dictionary
        # TODO: extract subset?
        # TODO: revisit flattening strategy
        data_flat = flatten_json.flatten(self.data, separator=self.FLATTEN_DELIMITER)

        # Ensure timestamp column not in data
        # NOTE: this field must be protected, otherwise the timestamp
        #       will not be interpreted safely from the line format
        if "timestamp" in data_flat.keys():
            del data_flat["timestamp"]

        # Sanitise keys
        for pair in self.SANTISED_KEYS:
            data_flat = {key.replace(*pair): value for key, value in data_flat.items()}

        # Return InfluxDB point
        return Point.from_dict(
            {
                "time": timestamp_ns,
                "measurement": self.event,
                "tags": self.tags,
                "fields": data_flat,
            }
        )

    # TODO: split into to_sanitised and to_point?

    # Delimiter when flattening data
    FLATTEN_DELIMITER = "__"

    # Sanitised forms of keys
    SANTISED_KEYS = [
        (" ", "_"),
        ("-", "____"),
    ]
