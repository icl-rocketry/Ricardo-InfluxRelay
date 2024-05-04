# Standard imports
from typing import Dict, Type

# Internal imports
from .file import FileHandler
from .handler import Handler
from .influxdb import InfluxDBHandler
from .manager import HandlerManager
from .print import PrintHandler

# Declare Handler mapping
HANDLER_MAP: Dict[str, Type[Handler]] = {
    "influxdb": InfluxDBHandler,
    "print": PrintHandler,
    "file": FileHandler,
}


def get_handler_type(name: str) -> Type[Handler]:
    # Get corresponding handler type
    handlerType = HANDLER_MAP.get(name, None)

    # Raise error for unknown handler type
    if handlerType is None:
        raise ValueError(f"Unknown handler type: {handlerType}")

    # Return handler
    return handlerType
