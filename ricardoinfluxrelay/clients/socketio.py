# Standard imports
import logging
from typing import Any, Dict, List, Set, Union

# Third-party imports
from socketio import AsyncClient

# Internal imports
from ricardoinfluxrelay.event import Event
from ricardoinfluxrelay.process import AsyncProcess


class SocketIOClient(AsyncProcess):

    def __init__(
        self,
        url: str,
        namespaces: Union[Set[str], List[str]],
        tags: Dict[str, str] = {},
        ssl_verify: bool = True,
        *args,
        **kwargs,
    ) -> None:
        # Initialise parent
        super().__init__(*args, **kwargs)

        # Store parameters
        self.url = url
        self.namespaces = namespaces
        self.tags = tags
        self.ssl_verify = ssl_verify

        # Declare connection time variable
        self.previousAttemptTime = 0

    async def _initialise(self) -> bool:
        # Declare SocketIO client
        # TODO: try to revert to async-based client?
        self.client = AsyncClient(handle_sigint=False, ssl_verify=self.ssl_verify)

        # Register (disconnection messages)
        self.client.on(event="connect", namespace="*", handler=self._connected)
        self.client.on(event="disconnect", namespace="*", handler=self._disconnected)

        # Register handler
        self.client.on(
            event="*",
            namespace="*",
            handler=self.handler,
        )

        # Connect client
        await self.connect()

        # Return success
        # NOTE: due to autoreconnect, this does not indicate whether the client connected successfully
        return True

    async def _deinitialise(self) -> None:
        # Disconnect client
        await self.disconnect()

    async def input(self, obj: Any) -> None:
        pass

    async def connect(self) -> None:
        # Log connection attempt
        logging.info(f"Attempting connection to {self.url}")

        # Connect client
        try:
            await self.client.connect(self.url, namespaces=self.namespaces, retry=True)
        except:
            # TODO: log failure to connect
            pass

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

    def handler(self, event: str, namespace: str, data: str) -> None:
        # Create event object
        eventObj = Event(namespace, event, data, self.tags)

        # Call event handler
        self.outputQueue.put_nowait(eventObj)
