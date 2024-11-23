# Standard imports
import asyncio
import json
import logging
from typing import Dict, List

# Third-party imports
import websockets

# Internal imports
from .handler import AsyncHandler
from ricardoinfluxrelay.event import Event


class WebSocketHandler(AsyncHandler):

    def __init__(
        self,
        namespaces: List[str],
        host: str,
        port: int,
        tags: Dict[str, str] = {},
        *args,
        **kwargs,
    ):
        # Initialise parent
        super().__init__(namespaces, tags, *args, **kwargs)

        # Store host and port
        self.host = host
        self.port = port

        # Create list of clients
        self.clients: List[WebSocketHanderClient] = []

    async def _initialise(self) -> bool:
        # Create server
        self.server = await websockets.serve(self._handler, self.host, self.port)

        # Log initialisation
        # TODO: add additional information
        logging.info("WebSocket handler initialised")

        # Return success
        return True

    async def _deinitialise(self) -> None:
        # TODO: stop server

        # Log deinitialisation
        # TODO: add additional information
        logging.info("WebSocket handler deinitialised")

    async def _handler(
        self,
        websocket: websockets.WebSocketServerProtocol,
        path: str,
    ):
        # Declare client (to prevent unbound behaviour)
        client = None

        # TODO: log connection

        try:
            # Create client object
            client = WebSocketHanderClient(websocket, path)

            # Append to client list
            self.clients.append(client)

            # Wait for connection with client to finish
            await websocket.wait_closed()
        finally:
            # Remove from client list
            if client is not None:
                self.clients.remove(client)

        # TODO: log disconnection

    async def _on_event(self, event: Event):
        # Extract data from event
        data = event.data

        # Add tags to data
        data["tags"] = event.tags

        # Re-serialise data
        message = json.dumps(data)

        # Send events
        tasks = [
            client.on_event(message)
            for client in self.clients
            if client.namespace == event.namespace and client.event == event.event
        ]

        # Wait for sends to finish
        await asyncio.gather(*tasks)

    async def update(self) -> None:
        # Add additional sleep to yield to event loop on every iteration
        # TODO: address this bodge
        await asyncio.sleep(10e-3)


class WebSocketHanderClient:

    def __init__(
        self,
        websocket: websockets.WebSocketServerProtocol,
        path: str,
    ) -> None:
        # Store websocket and path
        self.websocket = websocket
        self.path = path

        # Split namespace and event from path
        # TODO: requires better implementation
        split_path = path.split("/", 2)

        # Check path validity
        # TODO: requires better implementation
        if len(split_path) != 3:
            raise ValueError("Incorrect number of elements in path")
        if split_path[0] != "":
            raise ValueError(f"First element should be blank")

        # Store namespace and event
        self.namespace = "/" + split_path[1]
        self.event = split_path[2]

        # Fix for backwards compatibility
        # TODO: deprecate this eventually
        if self.namespace == "/ws":
            self.namespace = "/telemetry"

    async def on_event(self, message: str):
        # Send message
        await self.websocket.send(message)
