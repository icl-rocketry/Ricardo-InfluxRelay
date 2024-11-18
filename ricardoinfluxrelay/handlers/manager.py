# Standard imports
from dataclasses import dataclass
import logging
import multiprocessing as mp
from typing import Dict, List, Set, Sequence

# Internal imports
from .handler import Handler, HandlerProcess


@dataclass
class HandlerSet:
    handler: Handler
    queue: mp.Queue
    process: HandlerProcess

    @classmethod
    def generate(cls, handler: Handler):
        # Create queue
        queue = mp.Queue()

        # Generate process
        process = HandlerProcess(queue, handler)

        # Generate handler set
        return HandlerSet(handler, queue, process)


class HandlerManager:

    def __init__(self, handlers: Sequence[Handler]):
        # Create handler sets
        self.handlers = [HandlerSet.generate(handler) for handler in handlers]

        # Start processes
        self.start()

    def __del__(self):
        # Stop processes
        self.stop()

    def start(self):
        # Iterate through handlers
        for handler in self.handlers:
            # Start process
            handler.process.start()

    def stop(self):
        # Iterate through processes
        for handler in self.handlers:
            # Stop process
            handler.process.shutdown()

    def on_event(
        self,
        namespace: str,
        event: str,
        data: str,
        extra_tags: Dict[str, str],
    ):
        # Log event
        logging.debug(f"Received event {event} in {namespace}")

        # Iterate through handlers
        for handler in self.handlers:
            # Send event to queue
            # TODO: replace with dataclass?
            handler.queue.put(
                {
                    "namespace": namespace,
                    "event": event,
                    "data": data,
                    "extra_tags": extra_tags,
                }
            )

    @property
    def handlers(self) -> List[HandlerSet]:
        # Return handlers
        return self._handlers

    @handlers.setter
    def handlers(self, value: List[HandlerSet]):
        # Update handlers
        self._handlers = value

        # Update unique set of namespaces
        self.namespaces = set(
            [
                namespace
                for handler in self.handlers  # Iterate through handlers
                for namespace in handler.handler.namespaces  # Iterate through handler namespaces
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
