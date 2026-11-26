from app.scrub.catalog import RedactionCatalog

_CATALOG = RedactionCatalog()


class MockProvider:
    def __init__(self, name: str, label: str):
        self.name = name
        self.label = label

    def complete(self, text: str) -> str:
        if _CATALOG.findSpans(text):
            return (
                f"{self.label} received identifiable patient data. "
                "That text should have been redacted before send."
            )
        return (
            f"{self.label}: I can discuss tooth-care habits in general. "
            "The prompt I received used placeholders instead of patient identifiers."
        )
