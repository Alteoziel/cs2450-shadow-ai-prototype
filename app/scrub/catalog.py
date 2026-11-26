import re

from app.scrub.fake_word import FakeWord
from app.scrub.names import FIRST_NAMES, NOT_LAST_NAMES
from app.scrub.redaction_rule import RedactionRule

_NAME_PAIR = re.compile(r"\b([A-Za-z]{2,20})\s+([A-Za-z]{2,20})\b")
_TITLED_NAME = re.compile(
    r"\b(?:mr|mrs|ms|dr|patient)\.?\s+[A-Za-z]{2,20}(?:\s+[A-Za-z]{2,20})?\b",
    re.IGNORECASE,
)


def default_rules():
    specs = [
        ("ssn", r"\d{3}-\d{2}-\d{4}", "[SSN]"),
        ("email", r"[\w.+-]+@[\w.-]+\.\w+", "[EMAIL]"),
        (
            "phone",
            r"(?:\+?1[\s.-])?(?:\(\d{3}\)|\d{3})[\s.-]\d{3}[\s.-]\d{4}",
            "[PHONE]",
        ),
        ("creditCard", r"(?:\d{4}[\s-]){3}\d{4}", "[CARD]"),
        (
            "dateOfBirth",
            r"(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2}|\d{2}-\d{2}-\d{4})",
            "[DATE]",
        ),
        (
            "monthDate",
            r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+(?:19|20)\d{2}",
            "[DATE]",
        ),
        (
            "street",
            r"\d{1,5}\s+(?:[A-Za-z0-9.'-]+\s+){1,4}(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd|Way|Court|Ct)\b",
            "[ADDRESS]",
        ),
        ("patientName", r"Patient\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+", "[PATIENT]"),
    ]
    rules = []
    for rule_name, pattern, placeholder in specs:
        rules.append(RedactionRule(rule_name, pattern, FakeWord(placeholder, pattern)))
    return rules


def _overlaps(start, end, kept):
    return any(start < item["end"] and end > item["start"] for item in kept)


class RedactionCatalog:
    def __init__(self, rules=None):
        self.rules = default_rules() if rules is None else rules

    def findSpans(self, text: str):
        found = []
        for rule in self.rules:
            for match in rule.finditer(text):
                phrase = match.group()
                if rule.appliesTo(phrase) and rule.fakeWord.matches(phrase):
                    found.append(
                        {
                            "start": match.start(),
                            "end": match.end(),
                            "text": phrase,
                            "ruleName": rule.ruleName,
                            "placeholder": rule.fakeWord.fakeWord,
                            "fakeWord": rule.fakeWord,
                        }
                    )
        found.extend(self._name_spans(text))
        found.sort(key=lambda item: (item["start"], item["start"] - item["end"]))
        kept = []
        for span in found:
            if _overlaps(span["start"], span["end"], kept):
                continue
            kept.append(span)
        kept.sort(key=lambda item: item["start"])
        return kept

    def _name_spans(self, text: str):
        spans = []
        for match in _TITLED_NAME.finditer(text):
            spans.append(self._patient_span(match, "titledName"))
        for match in _NAME_PAIR.finditer(text):
            raw_first, raw_last = match.group(1), match.group(2)
            first, last = raw_first.lower(), raw_last.lower()
            title_pair = raw_first[:1].isupper() and raw_first[1:].islower() and raw_last[:1].isupper() and raw_last[1:].islower()
            if last in NOT_LAST_NAMES or first in NOT_LAST_NAMES:
                continue
            if first not in FIRST_NAMES and not title_pair:
                continue
            spans.append(self._patient_span(match, "personName"))
        return spans

    def _patient_span(self, match, rule_name):
        phrase = match.group()
        fake = FakeWord("[PATIENT]", re.escape(phrase))
        return {
            "start": match.start(),
            "end": match.end(),
            "text": phrase,
            "ruleName": rule_name,
            "placeholder": "[PATIENT]",
            "fakeWord": fake,
        }
