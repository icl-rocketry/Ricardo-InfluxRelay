# Standard imports
from typing import Dict

# Internal imports
from .handler import Handler


class PrintHandler(Handler):

    async def on_event(
        self,
        namespace: str,
        event: str,
        data: str,
        extra_tags: Dict[str, str] = {},
    ) -> None:
        # Generate tags
        tags = {**self.tags, **extra_tags}

        # Print event, data, and tags
        print({"namespace": namespace, "event": event, "data": data, "tags": tags})
