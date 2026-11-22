from app.proxy.providers.anthropic_adapter import AnthropicAdapter
from app.proxy.providers.mock_llm import MockProvider
from app.proxy.providers.openai_adapter import OpenAIAdapter

_MOCKS = {
    "mock-openai": ("mock-openai", "Mock OpenAI"),
    "mock-anthropic": ("mock-anthropic", "Mock Anthropic"),
}


def provider_for(model: str):
    if model in _MOCKS:
        name, label = _MOCKS[model]
        return MockProvider(name, label)
    if model == "openai":
        return OpenAIAdapter()
    if model == "anthropic":
        return AnthropicAdapter()
    return None
