# Standard imports
from abc import abstractmethod
import json
from typing import Any, Dict, List

# Internal imports
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

    def input(self, obj: Any) -> None:
        try:
            # Call event handler
            self.on_event(**obj)
        except:
            # TODO: log error
            pass
