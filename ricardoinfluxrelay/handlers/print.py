# Standard imports
import logging

# Internal imports
from .handler import Handler
from ricardoinfluxrelay.event import Event


class PrintHandler(Handler):

    def _initialise(self) -> bool:
        # Log initialisation
        # TODO: add additional information
        logging.info("Print handler initialised")

        # Return success
        return True

    def _deinitialise(self) -> None:
        # Log deinitialisation
        # TODO: add additional information
        logging.info("Print handler deinitialised")

    def _on_event(self, event: Event) -> None:
        # Log event
        logging.info(f"Data received: {event}")
