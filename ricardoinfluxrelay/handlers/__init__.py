# Standard imports
from typing import Type

# Internal imports
from .handler import Handler
from .influxdb import InfluxDBHandler
from .mixed import MixedHandler
from .print import PrintHandler
from .types import HANDLER_MAP, HANDLER_TYPES


def get_handler(name: str) -> Type[HANDLER_TYPES]:
    # Get corresponding handler
    handler = HANDLER_MAP.get(name, None)

    # Raise error for unknown handler
    if handler is None:
        raise ValueError(f"Unknown handler: {handler}")

    # Return handler
    return handler
