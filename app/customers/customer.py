class Customer:
    def __init__(self, name: str, allowed: bool = True):
        self.name = name
        self._allowed = allowed

    def canSend(self) -> bool:
        return self._allowed
