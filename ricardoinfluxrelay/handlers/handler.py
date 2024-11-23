# Standard imports
from abc import abstractmethod
from typing import Any, Dict, List

# Internal imports
from ricardoinfluxrelay.event import Event
from ricardoinfluxrelay.process import Process, AsyncProcess


class Handler(Process):
    def __init__(
        self,
        namespaces: List[str],
        tags: Dict[str, str] = {},
        *args,
        **kwargs,
    ) -> None:
        # Initialise parent
        super().__init__(*args, **kwargs)

        # Store namespaces
        self.namespaces = namespaces

        # Store tags
        self.tags = tags

    @abstractmethod
    def _on_event(self, event: Event) -> None: ...

    def on_event(self, event: Event) -> None:
        # Return if event namespace not in handler namespaces
        if event.namespace not in self.namespaces:
            return

        # Update tags
        event.tags = {**self.tags, **event.tags}

        # Execute event method
        self._on_event(event)

    def input(self, obj: Any) -> None:
        try:
            # Check object type
            # TODO: add message
            if not isinstance(obj, Event):
                raise ValueError

            # Call event handler
            self.on_event(obj)

        except:
            # TODO: log error
            pass


class AsyncHandler(AsyncProcess):
    def __init__(
        self,
        namespaces: List[str],
        tags: Dict[str, str] = {},
        *args,
        **kwargs,
    ) -> None:
        # Initialise parent
        super().__init__(*args, **kwargs)

        # Store namespaces
        self.namespaces = namespaces

        # Store tags
        self.tags = tags

    @abstractmethod
    async def _on_event(self, event: Event) -> None: ...

    async def on_event(self, event: Event) -> None:
        # Return if event namespace not in handler namespaces
        if event.namespace not in self.namespaces:
            return

        # Update tags
        event.tags = {**self.tags, **event.tags}

        # Execute event method
        await self._on_event(event)

    async def input(self, obj: Any) -> None:
        try:
            # Check object type
            # TODO: add message
            if not isinstance(obj, Event):
                raise ValueError

            # Call event handler
            await self.on_event(obj)

        except:
            # TODO: log error
            pass
