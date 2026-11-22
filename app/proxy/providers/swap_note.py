from datetime import datetime


class SwapNote:
    def __init__(self, model: str, fakeWords):
        self.savedAt = datetime.now()
        self.model = model
        self._fakeWords = list(fakeWords)

    def fakeWordUsed(self) -> str:
        return ", ".join(self._fakeWords)
