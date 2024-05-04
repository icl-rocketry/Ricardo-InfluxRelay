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

        # Store handler manager
        self.handler_manager = handler_manager

        # Iterate through namespaces
        for namespace in handler_manager.namespaces:
            # Create handler
            async def handler(event: str, data: str):
                # Call event handler
                return await self.handler_manager.on_event(namespace, event, data, tags)

            # Register handler
            self.client.on(
                event="*",
                namespace=namespace,
                handler=handler,
            )

    async def connect(self) -> None:
        # Connect client
        await self.client.connect(self.url, retry=True)

    async def disconnect(self) -> None:
        # Disconnect client
        await self.client.disconnect()

    async def wait(self) -> None:
        # Wait for connection to end
        await self.client.wait()
