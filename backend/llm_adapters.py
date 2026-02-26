# backend/llm_adapters.py
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import json

class LLMAdapter(ABC):
    """Abstract base class for LLM adapters."""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def generate(self, prompt: str, context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generates text based on a prompt and optional context.
        Returns a dictionary with at least 'text' and 'sources'.
        """
        pass

class OpenAIAdapter(LLMAdapter):
    """Adapter for OpenAI-compatible LLMs (e.g., GPT-3.5, GPT-4)."""
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-3.5-turbo"):
        super().__init__("openai_like", "OpenAI-compatible LLM")
        self.api_key = api_key # Use env var/secret management in production
        self.model_name = model_name

    def generate(self, prompt: str, context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # DUMMY IMPLEMENTATION FOR MVP: Replace with actual API call
        # In a real scenario, you'd use a library like 'openai' or 'requests'
        print(f"Calling OpenAI-like adapter for prompt: {prompt}")
        sources = context_data.get("sources", ["external_data"]) if context_data else ["external_data"]
        return {
            "text": f"Mock OpenAI-like output for prompt: '{prompt}'. Context sources: {', '.join(sources)}",
            "sources": sources + [self.name + f" ({self.model_name})"],
            "confidence": 0.85 # Mock confidence score
        }

class LocalMockAdapter(LLMAdapter):
    """A deterministic mock adapter for local testing or fallback."""
    def __init__(self):
        super().__init__("local_mock", "Deterministic mock LLM")

    def generate(self, prompt: str, context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        print(f"Calling LocalMock adapter for prompt: {prompt}")
        sources = context_data.get("sources", ["local_data"]) if context_data else ["local_data"]
        return {
            "text": f"Mock output from local LLM for prompt: '{prompt}'. Context sources: {', '.join(sources)}",
            "sources": sources + [self.name],
            "confidence": 1.0 # Mock is 100% confident for deterministic output
        }

class AdapterDispatcher:
    """Manages available LLM adapters and selects one based on configuration."""
    def __init__(self):
        # Instantiate adapters. API keys should be managed securely (e.g., env vars).
        self.adapters: Dict[str, LLMAdapter] = {
            "openai_like": OpenAIAdapter(model_name="gpt-3.5-turbo"),
            "local_mock": LocalMockAdapter()
        }
        self.default_adapter_key = "local_mock" # Fallback to mock if not specified
        self.selected_adapter_key = self.default_adapter_key

    def set_adapter(self, adapter_key: str):
        if adapter_key in self.adapters:
            self.selected_adapter_key = adapter_key
        else:
            print(f"Warning: Adapter '{adapter_key}' not found. Using default '{self.default_adapter_key}'.")
            self.selected_adapter_key = self.default_adapter_key

    def get_available_adapters(self) -> Dict[str, str]:
        """Returns a dict of adapter keys and their descriptions."""
        return {key: adapter.description for key, adapter in self.adapters.items()}

    def get_current_adapter_key(self) -> str:
        """Returns the currently selected adapter key."""
        return self.selected_adapter_key

    def generate(self, prompt: str, context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        adapter = self.adapters.get(self.selected_adapter_key)
        if not adapter:
            adapter = self.adapters.get(self.default_adapter_key)
            if not adapter:
                raise RuntimeError("No LLM adapters available.")
        return adapter.generate(prompt, context_data)

# Initialize dispatcher
LLM_DISPATCHER = AdapterDispatcher()
