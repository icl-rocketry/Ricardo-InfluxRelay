# Internal imports
from .handler import Handler


class PrintHandler(Handler):
    def __init__(self, namespace: str, *args, **kwargs) -> None:
        # Initialise parent
        super().__init__(namespace, *args, **kwargs)

    async def on_event(self, sid: str, data: str) -> None:
        # Print session ID and data
        print(sid, data)
