import re


class FakeWord:
    def __init__(self, fakeWord: str, pattern: str):
        self.fakeWord = fakeWord
        self._pattern = re.compile(pattern)

    def matches(self, phrase: str) -> bool:
        return self._pattern.fullmatch(phrase) is not None
