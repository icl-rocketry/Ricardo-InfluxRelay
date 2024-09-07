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
        # Extract timestamp (in nano-seconds)
        timestamp = int(data["timestamp"] * 1e6)

        # Flatten data dictionary
        data_flat = flatten_json.flatten(data, separator=self.FLATTEN_DELIMITER)

        # Sanitise keys
        for pair in self.SANTISED_KEYS:
            data_flat = {key.replace(*pair): value for key, value in data_flat.items()}

        # Return InfluxDB point
        return Point.from_dict(
            {
                "time": timestamp,
                "measurement": event,
                "tags": tags,
                "fields": data_flat,
            }
        )

    # Delimiter when flattening data
    FLATTEN_DELIMITER = "__"

    # Sanitised forms of keys
    SANTISED_KEYS = [
        (" ", "_"),
        ("-", "____"),
    ]
