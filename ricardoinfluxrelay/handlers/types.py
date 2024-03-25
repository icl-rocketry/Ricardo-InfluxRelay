# Standard imports
from typing import Union

# Internal imports
from .handler import Handler
from .influxdb import InfluxDBHandler
from .mixed import MixedHandler
from .print import PrintHandler

# Declare Handler mapping
HANDLER_MAP = {"print": PrintHandler, "influxdb": InfluxDBHandler}

# Declare handler types
# TODO: find cleaner solution
HANDLER_TYPES = Union[Handler, InfluxDBHandler, MixedHandler, PrintHandler]
