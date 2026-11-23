from app.proxy.providers.anthropic_adapter import AnthropicAdapter
from app.proxy.providers.gemini_adapter import GeminiAdapter
from app.proxy.providers.keys import FAKE_KEY, load_keys
from app.proxy.providers.mock_llm import MockProvider
from app.proxy.providers.openai_adapter import OpenAIAdapter

_MOCKS = {
    "mock-openai": ("mock-openai", "Mock OpenAI"),
    "mock-anthropic": ("mock-anthropic", "Mock Anthropic"),
}

OPENAI_MODELS = (
    ("gpt-4o-mini", "OpenAI · gpt-4o-mini"),
    ("gpt-4o", "OpenAI · gpt-4o"),
)
ANTHROPIC_MODELS = (
    ("claude-3-5-haiku-latest", "Anthropic · Claude Haiku"),
    ("claude-sonnet-4-5", "Anthropic · Claude Sonnet"),
)
GEMINI_MODELS = (
    ("gemini-2.5-flash", "Gemini · gemini-2.5-flash"),
    ("gemini-2.5-pro", "Gemini · gemini-2.5-pro"),
)


def available_models():
    models = [
        {"id": "mock-openai", "label": "Mock OpenAI", "company": "Mock"},
        {"id": "mock-anthropic", "label": "Mock Anthropic", "company": "Mock"},
    ]
    keys = load_keys()
    if keys["openai"]:
        models.extend(
            {"id": model_id, "label": label, "company": "OpenAI"}
            for model_id, label in OPENAI_MODELS
        )
    if keys["anthropic"]:
        models.extend(
            {"id": model_id, "label": label, "company": "Anthropic"}
            for model_id, label in ANTHROPIC_MODELS
        )
    if keys["gemini"]:
        models.extend(
            {"id": model_id, "label": label, "company": "Gemini"}
            for model_id, label in GEMINI_MODELS
        )
    return models


def _live_or_test(model: str, key: str, label: str, adapter):
    if not key:
        return None
    if key == FAKE_KEY:
        return MockProvider(model, f"{label} (test key)")
    return adapter(model, key)


def provider_for(model: str):
    if model in _MOCKS:
        name, label = _MOCKS[model]
        return MockProvider(name, label)
    keys = load_keys()
    openai_ids = {model_id for model_id, _label in OPENAI_MODELS}
    anthropic_ids = {model_id for model_id, _label in ANTHROPIC_MODELS}
    gemini_ids = {model_id for model_id, _label in GEMINI_MODELS}
    if model in openai_ids:
        return _live_or_test(model, keys["openai"], "OpenAI", OpenAIAdapter)
    if model in anthropic_ids:
        return _live_or_test(model, keys["anthropic"], "Anthropic", AnthropicAdapter)
    if model in gemini_ids:
        return _live_or_test(model, keys["gemini"], "Gemini", GeminiAdapter)
    return None
