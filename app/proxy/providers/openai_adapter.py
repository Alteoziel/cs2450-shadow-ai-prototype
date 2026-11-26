import json
import urllib.error
import urllib.request


class OpenAIAdapter:
    def __init__(self, model: str, api_key: str):
        self.name = model
        self.model = model
        self.api_key = api_key

    def complete(self, text: str) -> str:
        body = json.dumps(
            {"model": self.model, "messages": [{"role": "user", "content": text}]}
        ).encode()
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode())
            return payload["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as exc:
            return f"OpenAI refused the request ({exc.code}). The redacted prompt was not retried."
        except Exception:
            return "OpenAI could not be reached. The redacted prompt was not retried."
