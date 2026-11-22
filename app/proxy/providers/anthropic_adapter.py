import os


class AnthropicAdapter:
    name = "anthropic"

    def complete(self, text: str) -> str:
        if not os.getenv("ANTHROPIC_API_KEY"):
            return "Anthropic adapter is not built for this prototype. No request was sent."
        return "An Anthropic key is set, but the live adapter is not built. No request was sent."
