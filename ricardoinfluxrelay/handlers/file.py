# Standard imports
import os
from typing import Dict, List

# Internal imports
from .handler import Handler
from ricardoinfluxrelay.event import Event


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

    def initialise(self) -> None:
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(self.filepath)), exist_ok=True)

        # Open file (append mode)
        self.fid = open(self.filepath, "a")

    def deinitialise(self) -> None:
        # Close file
        self.fid.close()

    def _on_event(self, event: Event) -> None:
        # Convert data to point
        point = event.to_point()

        # TODO: check types?

        # Write point to file
        self.fid.write(str(point) + "\n")
