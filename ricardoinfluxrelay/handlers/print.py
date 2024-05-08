# Standard imports
from typing import Dict

# Internal imports
from .handler import Handler


class PrintHandler(Handler):

    async def _on_event(
        self,
        namespace: str,
        event: str,
        data: str,
        tags: Dict[str, str],
    ) -> None:
        # Print namespace, event, data, and tags
        print({"namespace": namespace, "event": event, "data": data, "tags": tags})
