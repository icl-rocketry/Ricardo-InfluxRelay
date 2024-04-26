# Standard imports
from typing import Dict, Sequence

# Third-party imports
from socketio import AsyncClient

# Internal imports
from ricardoinfluxrelay.handlers import Handler


class SocketRelay:
    def __init__(self, url: str, tags: Dict[str, str] = {}) -> None:
        # Declare socketio client
        self.client = AsyncClient()

        # Store URL and tags
        self.url = url
        self.tags = tags

    def add_handlers(self, handlers: Sequence[Handler]) -> None:
        # TODO: deal with repeated calls to add handlers

        # Extract namespaces
        namespaces = [handler.namespace for handler in handlers]

        # Check for repeated namespaces
        if len(set(namespaces)) != len(namespaces):
            raise ValueError("Repeated namespaces in handlers")

        # Iterate through handlers
        for handler in handlers:
            # Register handler
            self.client.on(
                event="*",
                namespace=handler.namespace,
                handler=handler.on_event,
            )

    async def connect(self) -> None:
        # Connect client
        await self.client.connect(self.url)

    async def disconnect(self) -> None:
        # Disconnect client
        await self.client.disconnect()
