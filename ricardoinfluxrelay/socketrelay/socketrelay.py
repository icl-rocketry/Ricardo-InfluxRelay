# Standard imports
from typing import Dict

# Third-party imports
from socketio import AsyncClient

# Internal imports
from ricardoinfluxrelay.handlers import HandlerManager


class SocketRelay:
    def __init__(
        self,
        url: str,
        handler_manager: HandlerManager,
        tags: Dict[str, str] = {},
        ssl_verify: bool = True,
    ) -> None:
        # Declare socketio client
        self.client = AsyncClient(handle_sigint=False, ssl_verify=ssl_verify)

        # Store URL and tags
        self.url = url
        self.tags = tags

        # Store handler manager and extract namespaces
        self.handler_manager = handler_manager
        self.namespaces = list(handler_manager.namespaces)

        # Create handler
        async def handler(event: str, namespace: str, data: str):
            # Call event handler
            await self.handler_manager.on_event(namespace, event, data, tags)

        # Register handler
        self.client.on(
            event="*",
            namespace="*",
            handler=handler,
        )

    async def connect(self) -> None:
        # Connect client
        await self.client.connect(self.url, namespaces=self.namespaces, retry=True)

        # Print connection message
        # TODO: replace with logger
        print(f"[{id(self)}] Connected to {self.url}")

    async def disconnect(self) -> None:
        # Disconnect client
        await self.client.disconnect()

        # Print disconnection method
        # TODO: replace with logger
        print(f"[{id(self)}] Disconnected from {self.url}")

    async def wait(self) -> None:
        # Wait for connection to end
        await self.client.wait()
