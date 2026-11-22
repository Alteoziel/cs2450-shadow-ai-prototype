from app.scrub.fake_word import FakeWord
from app.scrub.redaction_rule import RedactionRule


def default_rules():
    specs = [
        ("ssn", r"\d{3}-\d{2}-\d{4}", "[SSN]"),
        ("email", r"[\w.+-]+@[\w.-]+\.\w+", "[EMAIL]"),
        ("phone", r"\d{3}-\d{3}-\d{4}", "[PHONE]"),
        ("dateOfBirth", r"\d{2}/\d{2}/\d{4}", "[DATE]"),
        ("patientName", r"Patient\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+", "[PATIENT]"),
    ]
    rules = []
    for rule_name, pattern, placeholder in specs:
        rules.append(RedactionRule(rule_name, pattern, FakeWord(placeholder, pattern)))
    return rules


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
        found.sort(key=lambda item: item["start"])
        return found
