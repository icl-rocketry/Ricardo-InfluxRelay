# Future imports
from __future__ import annotations

# Standard imports
from copy import deepcopy
from typing import Dict, List, Sequence

# Third-party imports
import yaml

# Internal imports
from ricardoinfluxrelay.handlers import Handler, MixedHandler, get_handler_type
from ricardoinfluxrelay.socketrelay import SocketRelay


class Configuration:

    def __init__(self, configuration) -> None:
        # Validate configuration
        # TODO: implement

        # Split configuration
        handlersConfiguration = configuration["handlers"]
        socketsConfiguration = configuration["sockets"]

        # Generate handlers
        self.handlers = [
            Configuration.generate_handler(handlerConfiguration)
            for handlerConfiguration in handlersConfiguration
        ]

        # Generate sockets
        self.sockets = [
            Configuration.generate_socket(socketConfiguration)
            for socketConfiguration in socketsConfiguration
        ]

    def build_sockets(self) -> List[SocketRelay]:
        # Make a copy of the sockets
        sockets = deepcopy(self.sockets)

        # Group handlers
        groupedHandlers_ = Configuration.group_handlers(self.handlers)

        # Iterate through the sockets
        for socket in sockets:
            # Make a copy of the handlers
            groupedHandlers = deepcopy(groupedHandlers_)

            # Update handler tags
            [handler.update_tags(socket.tags) for handler in groupedHandlers]

            # Add handlers to socket
            socket.add_handlers(groupedHandlers)

        # Return sockets
        return sockets

    @staticmethod
    def group_handlers(handlers: Sequence[Handler]) -> List[MixedHandler]:
        # Declare dictionary for handlers grouped by namespace
        groups: Dict[str, List[Handler]] = {}

        # Iterate through handlers
        for handler in handlers:
            # Extract handler namespace
            namespace = handler.namespace

            # Ensure list exists for namespace
            if groups.get(namespace, None) is None:
                groups[namespace] = []

            # Append handler to corresponding namespace group
            groups[namespace].append(handler)

        # Return grouped handlers
        return [MixedHandler(group) for _, group in groups.items()]

    @staticmethod
    def generate_handler(configuration) -> Handler:
        # Make a copy of the configuration
        configurationCopy = deepcopy(configuration)

        # Extract handler type
        handlerType = configurationCopy["type"]

        # Extract handler class
        handlerClass = get_handler_type(handlerType)

        # Drop type
        del configurationCopy["type"]

        # Return handler
        return handlerClass(**configurationCopy)

    @staticmethod
    def generate_socket(configuration) -> SocketRelay:
        # Make a copy of the configuration
        configurationCopy = deepcopy(configuration)

        # Extract URL and tags
        url = configurationCopy["url"]
        tags = configurationCopy["tags"]

        # Return socket relay
        return SocketRelay(url, tags)

    @staticmethod
    def load_yaml(path: str) -> Configuration:
        # Load configuration YAML
        with open(path, "r") as fid:
            configuration = yaml.load(fid, Loader=yaml.CSafeLoader)

        # Return configuration
        return Configuration(configuration)
