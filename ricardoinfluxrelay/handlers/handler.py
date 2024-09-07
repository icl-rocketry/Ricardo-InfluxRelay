# Standard imports
from abc import ABC, abstractmethod
import json
from typing import Any, Dict, List


class Handler(ABC):
    def __init__(self, namespaces: List[str], tags: Dict[str, str] = {}) -> None:
        # Store namespaces
        self.namespaces = namespaces

        # Store tags
        self.tags = tags

    def update_tags(self, tags: Dict[str, str]) -> None:
        # Update tags
        self.tags.update(tags)

    @abstractmethod
    async def _on_event(
        self,
        namespace: str,
        event: str,
        data: Dict[str, Any],
        tags: Dict[str, str],
    ) -> None: ...

    async def on_event(
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
        await self._on_event(namespace, event, data_dict, tags)

    # Delimiter when flattening data
    FLATTEN_DELIMITER = "__"
