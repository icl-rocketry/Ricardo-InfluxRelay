# Standard imports
from abc import abstractmethod
from typing import Any, Dict, List

# Internal imports
from ricardoinfluxrelay.event import Event
from ricardoinfluxrelay.process import Process


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

        # Generate tags
        tags = {**self.tags, **extra_tags}

        # Create event object
        eventObj = Event(namespace, event, data, tags)

        # Execute event method
        self._on_event(eventObj)

    def input(self, obj: Any) -> None:
        try:
            # Call event handler
            self.on_event(**obj)
        except:
            # TODO: log error
            pass
