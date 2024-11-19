# Standard imports
from dataclasses import dataclass
import json
from typing import Any, Dict


@dataclass
class Event:
    namespace: str
    event: str
    data: Dict[str, Any]
    tags: Dict[str, str]

    def __init__(
        self,
        namespace: str,
        event: str,
        data: str | Dict[str, Any],
        tags: Dict[str, str],
    ) -> None:
        # TODO: type checks?

        # Store namespace
        self.namespace = namespace

        # Store event
        self.event = event

        # Store data
        if isinstance(data, str):
            self.data = json.loads(data)
        else:
            self.data = data

        # Store tags
        self.tags = tags

    def __str__(self) -> str:
        # Return stringified dictionary representation
        return str(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        # Return dictionary representation
        return {
            "namespace": self.namespace,
            "event": self.event,
            "data": self.data,
            "tags": self.tags,
        }
