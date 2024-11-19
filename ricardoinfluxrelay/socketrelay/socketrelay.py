# Standard imports
import logging
from typing import Dict

# Third-party imports
from socketio import AsyncClient

# Internal imports
from ricardoinfluxrelay.event import Event
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

        # Register (dis)connection messages
        self.client.on(event="connect", namespace="*", handler=self._connected)
        self.client.on(event="disconnect", namespace="*", handler=self._disconnected)

        # Create handler
        async def handler(event: str, namespace: str, data: str):
            # Create event object
            eventObj = Event(namespace, event, data, tags)

            # Call event handler
            self.handler_manager.on_event(eventObj)

        # Register handler
        self.client.on(
            event="*",
            namespace="*",
            handler=handler,
        )

    async def connect(self) -> None:
        # Log connection attempt
        logging.info(f"Attempting connection to {self.url}")

        # Connect client
        await self.client.connect(self.url, namespaces=self.namespaces, retry=True)

    async def disconnect(self) -> None:
        # Log disconnection attempt
        if self.client.connected:
            logging.info(f"Disconnecting from {self.url}")
        else:
            logging.info(f"Shutting down from {self.url}")

        # Disconnect client
        await self.client.shutdown()

    def _connected(self, namespace: str) -> None:
        # Log connection
        logging.info(f"Connected to {namespace} at {self.url}")

    def _disconnected(self, namespace: str) -> None:
        # Log disconnection
        logging.info(f"Disconnected from {namespace} at {self.url}")

    async def wait(self) -> None:
        # Wait for connection to end
        await self.client.wait()
