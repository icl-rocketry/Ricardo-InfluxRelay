# Standard imports
from abc import ABC, abstractmethod
from typing import Dict, List


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
        data: str,
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

        # Generate tags
        tags = {**self.tags, **extra_tags}

        # Execute event method
        await self._on_event(namespace, event, data, tags)
