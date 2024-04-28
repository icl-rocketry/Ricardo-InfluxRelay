# Standard imports
from abc import ABC, abstractmethod
from typing import Dict


class Handler(ABC):
    def __init__(
        self,
        namespace: str,
        tags: Dict[str, str] = {},
    ) -> None:
        # Store namespace
        self.namespace = namespace

        # Store tags
        self.tags = tags

    def update_tags(self, tags: Dict[str, str]) -> None:
        # Update tags
        self.tags.update(tags)

    @abstractmethod
    async def on_event(self, sid: str, data: str) -> None: ...
