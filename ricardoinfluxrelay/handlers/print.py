# Standard imports
import logging

# Internal imports
from .handler import Handler
from ricardoinfluxrelay.event import Event


class PrintHandler(Handler):

    def initialise(self) -> None:
        pass

    def deinitialise(self) -> None:
        pass

    def _on_event(self, event: Event) -> None:
        # Log namespace, event, data, and tags
        logging.info(f"Data received: {event}")
