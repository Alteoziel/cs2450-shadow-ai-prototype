import re

from app.scrub.fake_word import FakeWord


class RedactionRule:
    def __init__(self, ruleName: str, pattern: str, fakeWord: FakeWord):
        self.ruleName = ruleName
        self._pattern = re.compile(pattern)
        self.fakeWord = fakeWord

    def appliesTo(self, phrase: str) -> bool:
        return self._pattern.fullmatch(phrase) is not None

    def finditer(self, text: str):
        return self._pattern.finditer(text)
