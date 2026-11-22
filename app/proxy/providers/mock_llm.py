import re


_SENSITIVE = re.compile(
    r"\d{3}-\d{2}-\d{4}"
    r"|\d{3}-\d{3}-\d{4}"
    r"|[\w.+-]+@[\w.-]+\.\w+"
    r"|\d{2}/\d{2}/\d{4}"
    r"|Patient\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+"
)


class MockProvider:
    def __init__(self, name: str, label: str):
        self.name = name
        self.label = label

    def complete(self, text: str) -> str:
        if _SENSITIVE.search(text):
            return (
                f"{self.label} received identifiable patient data and answered using it. "
                "This is what the keep-original path sends."
            )
        return (
            f"{self.label}: I can discuss tooth-care habits in general. "
            "The prompt I received used placeholders instead of patient identifiers."
        )
