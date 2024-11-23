# Future imports
from __future__ import annotations

# Standard imports
from copy import deepcopy
import multiprocessing as mp
from time import sleep
from typing import Dict, Union

# Third-party imports
import yaml

# Internal imports
from ricardoinfluxrelay.clients import ClientManager, Client, AsyncClient, ClientFactory
from ricardoinfluxrelay.handlers import (
    HandlerManager,
    Handler,
    AsyncHandler,
    HandlerFactory,
)


class Relay:

    def __init__(
        self,
        clientManager: ClientManager,
        handlerManager: HandlerManager,
    ) -> None:
        # Store client and handler managers
        self.clientManager = clientManager
        self.handlerManager = handlerManager

        # Declare run event
        self.stopRelay = mp.Event()

    def initialise(self) -> None:
        # Start handlers
        self.handlerManager.start()

        # Start clients
        self.clientManager.start()

    def deinitialise(self) -> None:
        # Stop clients
        self.clientManager.stop()

        # Stop handlers
        self.handlerManager.stop()

    def run(self) -> None:
        # Initialise relay
        self.initialise()

        # Run loop
        while not self.stopRelay.is_set():
            # Get events from clients
            events = self.clientManager.get()

            # Continue if no events available
            if len(events) == 0:
                sleep(self.EMPTY_SLEEP)
                continue

            # Iterate through events
            for event in events:
                # Send event to handlers
                # TODO: error handling?
                self.handlerManager.on_event(event)

        # Deinitialise relay
        self.deinitialise()

    def shutdown(self) -> None:
        # Stop relay
        self.stopRelay.set()

    @classmethod
    def load_yaml(cls, path: str) -> Relay:
        # Load configuration YAML
        with open(path, "r") as fid:
            configuration = yaml.load(fid, Loader=yaml.CSafeLoader)

        # Split configuration
        handlerConfigurations = configuration["handlers"]
        clientConfigurations = configuration["clients"]

        # Create handlers
        handlers = [Relay.generate_handler(config) for config in handlerConfigurations]

        # Create handler manager
        handlerManager = HandlerManager(handlers)

        # Create clients
        sockets = [
            Relay.generate_client(config, namespaces=handlerManager.namespaces)
            for config in clientConfigurations
        ]

        # Create client manager
        clientManager = ClientManager(sockets)

        # Return relay
        return Relay(clientManager, handlerManager)

    # TODO: move elsewhere?
    @staticmethod
    def generate_handler(
        configuration: Dict[str, str],
        *args,
        **kwargs,
    ) -> Union[Handler, AsyncHandler]:
        # Make a copy of the configuration
        configurationCopy = deepcopy(configuration)

        # Extract handler type
        handlerType = configurationCopy["type"]

        # Drop type
        del configurationCopy["type"]

        # Return handler
        return HandlerFactory.create(handlerType, *args, **configurationCopy, **kwargs)

    # TODO: move elsewhere?
    @staticmethod
    def generate_client(
        configuration: Dict[str, str],
        *args,
        **kwargs,
    ) -> Union[Client, AsyncClient]:
        # Make a copy of the configuration
        configurationCopy = deepcopy(configuration)

        # Extract client type
        clientType = configurationCopy["type"]

        # Drop type
        del configurationCopy["type"]

        # Return client
        return ClientFactory.create(clientType, *args, **configurationCopy, **kwargs)

    # Empty queue sleep [s]
    EMPTY_SLEEP = 10e-3
