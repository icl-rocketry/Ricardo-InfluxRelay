# Standard imports
from abc import ABC, abstractmethod
import multiprocessing as mp
import queue
from typing import Any


class Process(ABC, mp.Process):

    def __init__(self, *args, **kwargs):
        # Initialise parent class
        # TODO: make daemon optional?
        super().__init__(daemon=True, *args, **kwargs)

        # Declare send and receive queues
        self.inputQueue = mp.Queue()
        self.outputQueue = mp.Queue()

        # Declare run event
        self.stopProcess = mp.Event()

    @abstractmethod
    def initialise(self) -> None: ...

    @abstractmethod
    def deinitialise(self) -> None: ...

    @abstractmethod
    def input(self, obj: Any) -> None: ...

    def output(self, obj: Any) -> None:
        # Put object on output queue
        self.outputQueue.put_nowait(obj)
    
    def shutdown(self) -> None:
        # Stop process
        self.stopProcess.set()

    def run(self) -> None:
        # Initialise process
        self.initialise()

        # Run loop
        while not self.stopProcess.is_set():
            try:
                # Get object from input queue
                obj = self.inputQueue.get(timeout=self.QUEUE_TIMEOUT)

                # Call input handler
                self.input(obj)

            except queue.Empty:
                # TODO: log empty queue?
                pass

            except:
                # TODO: handle other exceptions?
                pass

        # Deinitialise process
        self.deinitialise()

    def put(self, obj: Any, block: bool = True, timeout: float | None = None) -> None:
        # Put object on receive queue
        self.inputQueue.put(obj, block, timeout)

    def get(self, block: bool = True, timeout: float | None = None) -> Any:
        # Return object on send queue
        return self.outputQueue.get(block, timeout)

    # Queue timeout [s]
    QUEUE_TIMEOUT = 20e-3
