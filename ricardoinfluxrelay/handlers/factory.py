# Standard imports
from typing import Callable, Dict, Type, Union

# Internal imports
from .handler import Handler, AsyncHandler


class HandlerFactory:

    # Registry of handler types
    registry: Dict[str, Type[Union[Handler, AsyncHandler]]] = {}

    @classmethod
    def register(cls, name: str) -> Callable:

        def inner_wrapper(
            handler: Type[Union[Handler, AsyncHandler]]
        ) -> Type[Union[Handler, AsyncHandler]]:
            # Raise error if handler name already registered
            if name in cls.registry:
                raise RuntimeError(f"Handler {name} already registered")

            # Store handler name and type
            cls.registry[name] = handler

            # Return handler
            return handler

        # Return inner function
        return inner_wrapper

    @classmethod
    def create(cls, name: str, *args, **kwargs) -> Union[Handler, AsyncHandler]:
        # Raise error if handler not registered
        if name not in cls.registry:
            raise RuntimeWarning(f"Unknown handler: {name}")

        # Extract handler type
        handler = cls.registry[name]

        # Return initialised handler
        return handler(*args, **kwargs)
