import json
import urllib.error
import urllib.request


class AnthropicAdapter:
    def __init__(self, model: str, api_key: str):
        self.name = model
        self.model = model
        self.api_key = api_key

    def complete(self, text: str) -> str:
        body = json.dumps(
            {
                "model": self.model,
                "max_tokens": 400,
                "messages": [{"role": "user", "content": text}],
            }
        ).encode()
        request = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode())
            parts = payload.get("content") or []
            text_parts = [part.get("text", "") for part in parts if part.get("type") == "text"]
            return "\n".join(text_parts) or "Anthropic returned an empty reply."
        except urllib.error.HTTPError as exc:
            return f"Anthropic refused the request ({exc.code}). The redacted prompt was not retried."
        except Exception:
            return "Anthropic could not be reached. The redacted prompt was not retried."
