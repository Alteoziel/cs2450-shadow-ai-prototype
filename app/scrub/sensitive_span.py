from app.scrub.mapping import Mapping


class SensitiveSpan:
    def __init__(self, start: int, end: int, original: str, fakeWord):
        self.start = start
        self.end = end
        self.original = original
        self.fakeWord = fakeWord
        self.flagged = True
        self.mapping = None

    def replace(self) -> Mapping:
        self.mapping = Mapping(self.original, self.fakeWord.fakeWord)
        return self.mapping

    def removeFlag(self) -> str:
        self.flagged = False
        return self.original
