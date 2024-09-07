# Standard imports
import os
from typing import Any, Dict, List

# Internal imports
from .sanitised import SanitisedHandler


class FileHandler(SanitisedHandler):

    def __init__(self, namespaces: List[str], filepath: str, tags: Dict[str, str] = {}):
        # Ensure only a single namespace is provided
        if len(namespaces) != 1:
            raise ValueError(
                f"FileHandler only supports a single namespace ({len(namespaces)} requested)"
            )

        # Initialise parent
        super().__init__(namespaces, tags)

        # Ensure directory exists
        os.makedirs(
            os.path.dirname(os.path.abspath(filepath)),
            exist_ok=True,
        )

        # Open file (append mode)
        self.fid = open(filepath, "a")

    def __del__(self):
        # Close file
        self.fid.close()

    async def _on_event(
        self,
        namespace: str,
        event: str,
        data: Dict[str, Any],
        tags: Dict[str, str],
    ) -> None:
        # Convert data to point
        point = self._to_point(event, data, tags)

        # TODO: check types?

        # Write point to file
        self.fid.write(str(point) + "\n")
