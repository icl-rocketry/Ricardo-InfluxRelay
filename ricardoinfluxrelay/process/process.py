# Standard imports
from abc import ABC, abstractmethod
import multiprocessing as mp
import queue
from typing import Any, Union


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

        # Set initialisation flag
        self.initialised = False

    @abstractmethod
    def _initialise(self) -> bool: ...

    @abstractmethod
    def _deinitialise(self) -> None: ...

    def initialise(self) -> None:
        # Return if already initialised
        if self.initialised:
            return

        # Initialise process
        self.initialised = self._initialise()

    def deinitialise(self) -> None:
        # Return if already deinitialised
        if not self.initialised:
            return

        # Deinitialise process
        self._deinitialise()

    @abstractmethod
    def input(self, obj: Any) -> None: ...

    def output(self, obj: Any) -> None:
        # Put object on output queue
        self.outputQueue.put_nowait(obj)

    def update(self) -> None:
        pass

    def shutdown(self) -> None:
        # Stop process
        self.stopProcess.set()

    def process_queues(self, drop: bool = True) -> None:
        # To prevent the input queue from filling up, objects can be optionally "dropped" without the input method being called
        #
        #  ============= ======= ============================================
        #   Initialised   Drop    Result
        #  ============= ======= ============================================
        #   False         False   No action
        #   False         True    Object taken from queue, no further action
        #   True          False   Input method called
        #   True          True    "
        #  ============= ======= ============================================
        #

        # Return if process is deinitialised and dropping is disabled
        if (not self.initialised) and (not drop):
            return

        try:
            # Get object from input queue
            obj = self.inputQueue.get(timeout=self.QUEUE_TIMEOUT)

            # Return if not initialised
            # TODO: move to input method?
            if not self.initialised:
                return

            # Call input handler
            self.input(obj)

        except queue.Empty:
            # TODO: log empty queue?
            pass

        except:
            # TODO: handle other exceptions?
            pass

    def run(self) -> None:
        # Initialise process
        self.initialise()

        # Run loop
        while not self.stopProcess.is_set():
            # Process input queue
            self.process_queues()

            # Continue run loop if not initialised
            if not self.initialised:
                continue

            # Update process
            # NOTE: only called when initialised
            self.update()

        # Deinitialise process
        self.deinitialise()

    def put(
        self,
        obj: Any,
        block: bool = True,
        timeout: Union[float, None] = None,
    ) -> None:
        # Put object on receive queue
        self.inputQueue.put(obj, block, timeout)

    def get(
        self,
        block: bool = True,
        timeout: Union[float, None] = None,
    ) -> Any:
        # Return object on send queue
        return self.outputQueue.get(block, timeout)

    # Queue timeout [s]
    QUEUE_TIMEOUT = 20e-3
