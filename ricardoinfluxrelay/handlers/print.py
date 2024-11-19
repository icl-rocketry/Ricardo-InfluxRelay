# Standard imports
import logging
from typing import Any, Dict

# Internal imports
from .handler import Handler


class PrintHandler(Handler):

    def initialise(self) -> None:
        pass

    def deinitialise(self) -> None:
        pass

    def _on_event(
        self,
        namespace: str,
        event: str,
        data: Dict[str, Any],
        tags: Dict[str, str],
    ) -> None:
        # Generate message
        message = str(
            {
                "namespace": namespace,
                "event": event,
                "data": data,
                "tags": tags,
            }
        )

        # Log namespace, event, data, and tags
        logging.info(f"Data received: {message}")
