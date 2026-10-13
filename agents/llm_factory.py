"""
Deterministic mock response provider with limited sensitive-pattern checks.
"""
from typing import Dict, Any, Optional
from .base import PHIGuard


class MockLLM:
    def __init__(self, system_name: str = "Threshold Ecdsa Ed25519 Agent"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return f"[{self.system_name}]: Mock response only; no clinical, cryptographic, or standards verification has been performed. Query: '{prompt[:60]}...'."


class LLMFactory:
    """Only deterministic mock responses are implemented; real providers are unsupported."""

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Threshold Ecdsa Ed25519 Agent"):
        prov = str(provider).lower()
        if prov in ["mock", "deterministic", "test"]:
            return MockLLM(system_name)
        raise ValueError(f"Unsupported model provider {provider!r}: only the deterministic mock is implemented.")
