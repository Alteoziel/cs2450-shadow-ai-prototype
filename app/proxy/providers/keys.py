import json
from pathlib import Path

_PATH = Path(__file__).resolve().parents[3] / "data" / "providers.json"
COMPANIES = ("openai", "anthropic", "gemini")
FAKE_KEY = "shadow-test"


def _blank() -> dict:
    return {name: "" for name in COMPANIES}


def load_keys() -> dict:
    current = _blank()
    if not _PATH.exists():
        return current
    try:
        saved = json.loads(_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return current
    for name in COMPANIES:
        current[name] = saved.get(name) or ""
    return current


def save_keys(openai: str = "", anthropic: str = "", gemini: str = "") -> None:
    _PATH.parent.mkdir(parents=True, exist_ok=True)
    current = load_keys()
    updates = {"openai": openai, "anthropic": anthropic, "gemini": gemini}
    for name, value in updates.items():
        if value:
            current[name] = value
    _PATH.write_text(json.dumps(current), encoding="utf-8")


def clear_key(company: str) -> None:
    current = load_keys()
    if company in current:
        current[company] = ""
    _PATH.parent.mkdir(parents=True, exist_ok=True)
    _PATH.write_text(json.dumps(current), encoding="utf-8")


def key_state(value: str) -> str:
    if not value:
        return "none"
    if value == FAKE_KEY:
        return "test"
    return "saved"


def key_status() -> dict:
    keys = load_keys()
    status = {name: key_state(keys[name]) for name in COMPANIES}
    status["fakeKey"] = FAKE_KEY
    return status
