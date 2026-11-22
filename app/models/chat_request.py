class ChatRequest:
    def __init__(self, text: str, model: str, officeActive: bool = True):
        self.text = text
        self.model = model
        self.officeActive = officeActive

    @classmethod
    def from_dict(cls, body: dict):
        office = body.get("officeActive", True)
        return cls(
            text=body.get("text") or "",
            model=body.get("model") or "mock-openai",
            officeActive=bool(office),
        )
