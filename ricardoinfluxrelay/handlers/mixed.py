# Standard imports
import asyncio
from typing import Dict, Sequence

# Internal imports
from .handler import Handler


class MixedHandler(Handler):
    def __init__(self, handlers: Sequence[Handler], *args, **kwargs) -> None:
        # Extract namespaces
        namespaces = [handler.namespace for handler in handlers]

        # Ensure single common namespace
        if len(set(namespaces)) != 1:
            raise ValueError("Non-singular namespaces")

        # Extract namespace
        namespace = namespaces[0]

        # Store handlers
        self.handlers = handlers

        # Initialise parent
        super().__init__(namespace, *args, **kwargs)

    def update_tags(self, tags: Dict[str, str]) -> None:
        # Update tags
        [handler.update_tags(tags) for handler in self.handlers]

    async def on_event(self, sid: str, data: str) -> None:
        # Spawn handler tasks
        tasks = [handler.on_event(sid, data) for handler in self.handlers]

        # Wait for tasks to complete
        await asyncio.gather(*tasks)
