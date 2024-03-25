# Standard imports
from typing import Sequence

# Third-party imports
from socketio import AsyncClient

# Internal imports
from ricardoinfluxrelay.handlers import HANDLER_TYPES


class SocketRelay:
    def __init__(self, handlers: Sequence[HANDLER_TYPES]):
        # Declare socketio client
        self.client = AsyncClient()

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

    async def connect(self, url: str) -> None:
        # Connect client
        await self.client.connect(url)

    async def disconnect(self) -> None:
        # Disconnect client
        await self.client.disconnect()
