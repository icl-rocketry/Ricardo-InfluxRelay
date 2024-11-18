# Standard imports
from typing import Any, Dict

# Third-party imports
import flatten_json
from influxdb_client import Point

# Internal imports
from .handler import Handler


class SanitisedHandler(Handler):

    def _to_point(
        self,
        event: str,
        data: Dict[str, Any],
        tags: Dict[str, str],
    ) -> Point:
        # Extract timestamp
        timestamp = data["timestamp"]
        timestamp_ns = int(timestamp * 1e6)

        # Flatten data dictionary
        # TODO: extract subset?
        data_flat = flatten_json.flatten(data, separator=self.FLATTEN_DELIMITER)

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
                "measurement": event,
                "tags": tags,
                "fields": data_flat,
            }
        )

    # TODO: revisit flattening strategy

    # Delimiter when flattening data
    FLATTEN_DELIMITER = "__"

    # Sanitised forms of keys
    SANTISED_KEYS = [
        (" ", "_"),
        ("-", "____"),
    ]
