# Standard imports
from abc import ABC, abstractmethod
from typing import Dict


class Handler(ABC):
    def __init__(self, namespace: str, *args, **kwargs) -> None:
        # Store namespace
        self.namespace = namespace

    @abstractmethod
    async def on_event(self, sid: str, data: str) -> None: ...


class TaggedHandler(Handler):

    def __init__(self, namespace: str, tags: Dict[str, str], *args, **kwargs) -> None:
        # Initialise parent class
        super().__init__(namespace, *args, **kwargs)

        # Store tags
        self.tags = tags
