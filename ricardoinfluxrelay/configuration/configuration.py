# Future imports
from __future__ import annotations

# Standard imports
from copy import deepcopy
from typing import Dict, List

# Third-party imports
import yaml

# Internal imports
from ricardoinfluxrelay.handlers import Handler, HandlerManager, get_handler_type
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

        # Create handler manager
        self.handler_manager = HandlerManager(self.handlers)

        # Generate sockets
        self.sockets = [
            Configuration.generate_socket(socketConfiguration, self.handler_manager)
            for socketConfiguration in socketsConfiguration
        ]

    def get_sockets(self) -> List[SocketRelay]:
        # Return sockets
        return self.sockets

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
    def generate_socket(configuration, handler_manager: HandlerManager) -> SocketRelay:
        # Make a copy of the configuration
        configurationCopy = deepcopy(configuration)

        # Extract URL and tags
        url: str = configurationCopy["url"]
        tags: Dict[str, str] = configurationCopy["tags"]
        ssl_verify: bool = configurationCopy["ssl_verify"]

        # Return socket relay
        return SocketRelay(
            url=url,
            handler_manager=handler_manager,
            tags=tags,
            ssl_verify=ssl_verify,
        )

    @staticmethod
    def load_yaml(path: str) -> Configuration:
        # Load configuration YAML
        with open(path, "r") as fid:
            configuration = yaml.load(fid, Loader=yaml.CSafeLoader)

        # Return configuration
        return Configuration(configuration)
