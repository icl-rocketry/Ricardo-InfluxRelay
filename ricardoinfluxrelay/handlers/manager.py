# Standard imports
import logging
from typing import Set, Sequence

# Internal imports
from .handler import Handler
from ricardoinfluxrelay.event import Event


class HandlerManager:

    def __init__(self, handlers: Sequence[Handler]):
        # Store handlers
        self.handlers = handlers

    def __del__(self) -> None:
        # Stop processes
        self.stop()

    def start(self) -> None:
        # Iterate through handlers
        for handler in self.handlers:
            # Start process
            handler.start()

    def stop(self) -> None:
        # Iterate through processes
        for handler in self.handlers:
            # Stop process
            handler.shutdown()

    def on_event(self, event: Event) -> None:
        # Log event
        logging.debug(f"Received event {event.event} in {event.namespace}")

        # Iterate through handlers
        for handler in self.handlers:
            # Send event to queue
            handler.put(event, block=False)

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
                for handler in self.handlers  # Iterate through handlers
                for namespace in handler.namespaces  # Iterate through handler namespaces
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
