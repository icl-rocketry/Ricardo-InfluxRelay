# Standard imports
from typing import Dict, Type, Union

# Internal imports
from .client import Client, AsyncClient
from .manager import ClientManager
from .socketio import SocketIOClient


# Declare Client mapping
CLIENT_MAP: Dict[str, Type[Union[Client, AsyncClient]]] = {
    "socketio": SocketIOClient,
}


def get_client_type(name: str) -> Type[Union[Client, AsyncClient]]:
    # Get corresponding client type
    clientType = CLIENT_MAP.get(name, None)

    # Raise error for unknown client type
    if clientType is None:
        raise ValueError(f"Unknown client type: {clientType}")

    # Return client type
    return clientType
