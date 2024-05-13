# Standard imports
import asyncio
import json
from typing import Dict, List

# Third-party imports
import websockets

# Internal imports
from .handler import Handler


class WebSocketHandler(Handler):

    def __init__(
        self,
        namespaces: List[str],
        host: str,
        port: int,
        tags: Dict[str, str] = {},
    ):
        # Initialise parent
        super().__init__(namespaces, tags)

        # Store host and port
        self.host = host
        self.port = port

        # Create list of clients
        self.clients: List[WebSocketHanderClient] = []

        # Create server
        self.server = websockets.serve(self.handler, host, port)

        # Start server
        asyncio.get_event_loop().run_until_complete(self.server)

    async def handler(
        self,
        websocket: websockets.WebSocketServerProtocol,
        path: str,
    ):
        # Declare client (to prevent unbound behaviour)
        client = None

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

    async def _on_event(
        self,
        namespace: str,
        event: str,
        data: str,
        tags: Dict[str, str],
    ):
        # Convert data string to dictionary
        packet = json.loads(data)

        # Add tags to packet
        packet["tags"] = tags

        # Re-serialise packet
        message = json.dumps(packet)

        # Spawn send tasks
        tasks = [
            client.on_event(message)
            for client in self.clients
            if client.namespace == namespace and client.event == event
        ]

        # Wait for sends to finish
        await asyncio.gather(*tasks)


class WebSocketHanderClient:
    # TODO: inherit from Handler class

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
            raise ValueError
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
