# Standard imports
import logging
import os
from typing import Dict, List

# Internal imports
from .factory import HandlerFactory
from .handler import Handler
from ricardoinfluxrelay.event import Event


@HandlerFactory.register("file")
class FileHandler(Handler):

    def __init__(
        self,
        namespaces: List[str],
        filepath: str,
        tags: Dict[str, str] = {},
        *args,
        **kwargs,
    ):
        # Ensure only a single namespace is provided
        if len(namespaces) != 1:
            raise ValueError(
                "FileHandler only supports a single namespace"
                + " "
                + f"({len(namespaces)} requested)"
            )

        # Initialise parent
        super().__init__(namespaces, tags, *args, **kwargs)

        # Store filepath
        self.filepath = filepath

    def _initialise(self) -> bool:
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(self.filepath)), exist_ok=True)

            # Open file (append mode)
            self.fid = open(self.filepath, "a")

            # Log initialisation
            # TODO: add additional information
            logging.info("File handler initialised")

            # Return success
            return True
        except:
            # Log initialisation failure
            logging.error("File handler failed to initialise")

            # Return failure
            return False

    def _deinitialise(self) -> None:
        # Close file
        self.fid.close()

        # Log deinitialisation
        # TODO: add additional information
        logging.info("File handler deinitialised")

    def _on_event(self, event: Event) -> None:
        # Convert data to point
        point = event.to_point()

        # TODO: check types?

        # Write point to file
        self.fid.write(str(point) + "\n")
