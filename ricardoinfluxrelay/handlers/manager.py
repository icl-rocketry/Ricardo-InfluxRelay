# Standard imports
import asyncio
import logging
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
        # Log event
        logging.debug(f"Received event {event} in {namespace}")

        # Generate handler tasks
        tasks = [
            handler.on_event(namespace, event, data, extra_tags)
            for handler in self.handlers
        ]

        # Execute handler tasks
        await asyncio.gather(*tasks)

    @property
    def handlers(self) -> Sequence[Handler]:
        # Return handlers
        return self._handlers

    @handlers.setter
    def handlers(self, value: Sequence[Handler]):
        # Update handlers
        self._handlers = value

        # Update unique set of namespaces
        self.namespaces = set(
            [
                namespace
                for handler in self.handlers  # iterate through handlers
                for namespace in handler.namespaces  # iterate through handler namespaces
            ]
        )

    @property
    def namespaces(self) -> Set[str]:
        # Return namespaces
        return self._namespaces

    @namespaces.setter
    def namespaces(self, value: Set[str]):
        # Set namespaces
        self._namespaces = value
