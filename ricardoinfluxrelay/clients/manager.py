# Standard imports
from typing import List

# Internal imports
from .socketio import SocketIOClient
from ricardoinfluxrelay.event import Event

# TODO: make generic client class


class ClientManager:

    def __init__(self, clients: List[SocketIOClient]) -> None:
        # Store clients
        self.clients = clients

    def __del__(self) -> None:
        # Stop processes
        self.stop()

    def start(self) -> None:
        # Iterate through clients
        for clients in self.clients:
            # Start process
            clients.start()

    def stop(self) -> None:
        # Iterate through clients
        for clients in self.clients:
            # Stop process
            clients.shutdown()

    def get(self) -> List[Event]:
        # Declare events list
        events = []

        # Iterate through clients
        for client in self.clients:
            # Iterate through event queue
            for _ in range(self.QUEUE_ITERATION_LIMIT):
                try:
                    # Get event
                    event = client.get(block=False)

                    # Append to events list
                    events.append(event)
                except:
                    # Break event queue loop
                    break

        # Return events list
        return events

    # Queue iteration limit
    QUEUE_ITERATION_LIMIT = 10
