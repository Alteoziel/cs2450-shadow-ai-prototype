import os


class OpenAIAdapter:
    name = "openai"

    def complete(self, text: str) -> str:
        if not os.getenv("OPENAI_API_KEY"):
            return "OpenAI adapter is not built for this prototype. No request was sent."
        return "An OpenAI key is set, but the live adapter is not built. No request was sent."
