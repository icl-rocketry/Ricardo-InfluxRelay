# Internal imports
from .handler import Handler


class PrintHandler(Handler):

    async def on_event(self, sid: str, data: str) -> None:
        # Print session ID and data
        print(sid, data)
