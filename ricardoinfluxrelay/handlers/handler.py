class Handler:
    def __init__(self, namespace: str, *args, **kwargs) -> None:
        # Store namespace
        self.namespace = namespace

    async def on_event(self, sid: str, data: str) -> None:
        # Throw error if not implemented
        raise NotImplementedError
