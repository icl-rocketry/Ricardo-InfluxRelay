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
    async def on_event(
        self,
        namespace: str,
        event: str,
        data: str,
        extra_tags: Dict[str, str] = {},
    ) -> None: ...
