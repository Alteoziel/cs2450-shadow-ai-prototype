import json
import urllib.error
import urllib.request


class GeminiAdapter:
    def __init__(self, model: str, api_key: str):
        self.name = model
        self.model = model
        self.api_key = api_key

    def complete(self, text: str) -> str:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )
        body = json.dumps(
            {"contents": [{"parts": [{"text": text}]}]}
        ).encode()
        request = urllib.request.Request(
            url,
            data=body,
            headers={
                "x-goog-api-key": self.api_key,
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode())
            parts = payload["candidates"][0]["content"]["parts"]
            reply = "".join(part.get("text", "") for part in parts).strip()
            return reply or "Gemini returned an empty reply."
        except urllib.error.HTTPError as exc:
            return f"Gemini refused the request ({exc.code}). The redacted prompt was not retried."
        except Exception:
            return "Gemini could not be reached. The redacted prompt was not retried."
