# Standard imports
from typing import Dict, Type, Union

# Internal imports
from .file import FileHandler
from .handler import AsyncHandler, Handler
from .influxdb import InfluxDBHandler
from .manager import HandlerManager
from .print import PrintHandler
from .websocket import WebSocketHandler

# Declare Handler mapping
HANDLER_MAP: Dict[str, Type[Union[Handler, AsyncHandler]]] = {
    "influxdb": InfluxDBHandler,
    "print": PrintHandler,
    "file": FileHandler,
    "websocket": WebSocketHandler,
}


def get_handler_type(name: str) -> Type[Union[Handler, AsyncHandler]]:
    # Get corresponding handler type
    handlerType = HANDLER_MAP.get(name, None)

    # Raise error for unknown handler type
    if handlerType is None:
        raise ValueError(f"Unknown handler type: {handlerType}")

    # Return handler
    return handlerType
