# Standard imports
from typing import Callable, Dict, Type, Union

# Internal imports
from .client import Client, AsyncClient


class ClientFactory:

    # Registry of client types
    registry: Dict[str, Type[Union[Client, AsyncClient]]] = {}

    @classmethod
    def register(cls, name: str) -> Callable:

        def inner_wrapper(
            client: Type[Union[Client, AsyncClient]]
        ) -> Type[Union[Client, AsyncClient]]:
            # Raise error if client name already registered
            if name in cls.registry:
                raise RuntimeError(f"Client {name} already registered")

            # Store client name and type
            cls.registry[name] = client

            # Return client
            return client

        # Return inner function
        return inner_wrapper

    @classmethod
    def create(cls, name: str, *args, **kwargs) -> Union[Client, AsyncClient]:
        # Raise error if client not registered
        if name not in cls.registry:
            raise RuntimeWarning(f"Unknown client: {name}")

        # Extract client type
        client = cls.registry[name]

        # Return initialised client
        return client(*args, **kwargs)
