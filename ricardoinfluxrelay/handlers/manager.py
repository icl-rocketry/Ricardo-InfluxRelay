# Standard imports
import asyncio
from typing import Dict, Set, Sequence

# Internal imports
from .handler import Handler


class HandlerManager:

    def __init__(self, handlers: Sequence[Handler]):
        # Store handlers
        self.handlers = handlers

    async def on_event(
        self,
        namespace: str,
        event: str,
        data: str,
        extra_tags: Dict[str, str],
    ):
        # Generate handler tasks
        tasks = [
            handler.on_event(event, data, extra_tags)
            for handler in self.handlers
            if handler.namespace == namespace
        ]

        # Execute handler tasks
        await asyncio.gather(*tasks)

    @property
    def handlers(self) -> Sequence[Handler]:
        # Return handlers
        return self._handlers

    @handlers.setter
    def handlers(self, value: Sequence[Handler]):
        # Update handlers and namespaces
        self._handlers = value
        self.namespaces = set([handler.namespace for handler in self.handlers])

    @property
    def namespaces(self) -> Set[str]:
        # Return namespaces
        return self._namespaces

    @namespaces.setter
    def namespaces(self, value: Set[str]):
        # Set namespaces
        self._namespaces = value
