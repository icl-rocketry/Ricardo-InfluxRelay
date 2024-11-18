# Standard imports
from abc import ABC, abstractmethod
import json
import multiprocessing as mp
import queue
from typing import Any, Dict, List


class Handler(ABC):
    def __init__(
        self,
        namespaces: List[str],
        tags: Dict[str, str] = {},
    ) -> None:
        # Store namespaces
        self.namespaces = namespaces

        # Store tags
        self.tags = tags

    def __del__(self):
        # Ensure handler is stopped
        self.stop()

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    @abstractmethod
    def _on_event(
        self,
        namespace: str,
        event: str,
        data: Dict[str, Any],
        tags: Dict[str, str],
    ) -> None: ...

    def on_event(
        self,
        namespace: str,
        event: str,
        data: str,
        extra_tags: Dict[str, str],
    ) -> None:
        # Return if event namespace not in handler namespaces
        if namespace not in self.namespaces:
            return

        # Convert data to dictionary
        # NOTE: in theory, this ensures that each handler has its own unique
        #       copy of the data, meaning that it can be modified later
        data_dict: Dict[str, Any] = json.loads(data)

        # Generate tags
        tags = {**self.tags, **extra_tags}

        # Execute event method
        self._on_event(namespace, event, data_dict, tags)


class HandlerProcess(mp.Process):

    def __init__(
        self,
        queue: mp.Queue,
        handler: Handler,
        *args,
        **kwargs,
    ) -> None:
        # Initialise parent
        super().__init__(daemon=True, *args, **kwargs)

        # Store event queue
        self.queue = queue

        # Store handler
        self.handler = handler

        # Declare stop event
        self.stop = mp.Event()

    def run(self):
        # Start handler
        self.handler.start()

        # Run loop while stop event is not set
        while not self.stop.is_set():
            try:
                # Get event from queue
                event = self.queue.get(timeout=self.QUEUE_TIMEOUT)

                # Check for sentinel
                if event is self.SENTINEL:
                    # Set stop event
                    self.stop.set()
                    continue

                # Call handler event
                self.handler.on_event(**event)

            except queue.Empty:
                # TODO: log empty queue?
                pass

            except:
                # TODO: handle other exceptions?
                pass

        # Stop handler
        self.handler.stop()

    def shutdown(self):
        # Set stop event
        self.stop.set()

    # Sentinel to stop process
    SENTINEL = None

    # Queue timeout [s]
    QUEUE_TIMEOUT = 20e-3
