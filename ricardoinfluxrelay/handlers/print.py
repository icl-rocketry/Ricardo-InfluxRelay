# Standard imports
from typing import Any, Dict

# Internal imports
from .handler import Handler


class PrintHandler(Handler):

    async def _on_event(
        self,
        namespace: str,
        event: str,
        data: Dict[str, Any],
        tags: Dict[str, str],
    ) -> None:
        # Print namespace, event, data, and tags
        print({"namespace": namespace, "event": event, "data": data, "tags": tags})
