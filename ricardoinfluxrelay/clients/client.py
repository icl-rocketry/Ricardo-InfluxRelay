# Internal imports
from ricardoinfluxrelay.process import Process, AsyncProcess


class Client(Process):

    def __init__(self, *args, **kwargs) -> None:
        # Initialise parent
        super().__init__(*args, **kwargs)


class AsyncClient(AsyncProcess):

    def __init__(self, *args, **kwargs) -> None:
        # Initialise parent
        super().__init__(*args, **kwargs)
