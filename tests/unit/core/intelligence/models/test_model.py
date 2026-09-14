from __future__ import annotations

import pytest

from dobby.core.intelligence.models.model import (
    Model,
    ModelCapability,
    ModelRequest,
    ModelResponse,
)


class FakeModel(Model):
    """Minimal model implementation for model contract tests."""

    @property
    def name(self) -> str:
        return "fake-model"

    @property
    def capabilities(self) -> frozenset[ModelCapability]:
        return frozenset(
            {
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CODING,
            }
        )


def test_model_exposes_name() -> None:
    model = FakeModel()

    assert model.name == "fake-model"


def test_model_exposes_capabilities() -> None:
    model = FakeModel()

    assert ModelCapability.TEXT_GENERATION in model.capabilities
    assert ModelCapability.CODING in model.capabilities


def test_model_supports_capability() -> None:
    model = FakeModel()

    assert model.supports(ModelCapability.TEXT_GENERATION)
    assert model.supports(ModelCapability.CODING)


def test_model_rejects_unsupported_capability() -> None:
    model = FakeModel()

    assert not model.supports(ModelCapability.VISION)


def test_model_request_requires_prompt() -> None:
    with pytest.raises(ValueError, match="prompt cannot be empty"):
        ModelRequest(prompt="   ")


def test_model_request_rejects_negative_temperature() -> None:
    with pytest.raises(
        ValueError,
        match="temperature cannot be negative",
    ):
        ModelRequest(
            prompt="Hello Dobby",
            temperature=-0.1,
        )


def test_model_request_rejects_invalid_max_tokens() -> None:
    with pytest.raises(
        ValueError,
        match="max_tokens must be greater than zero",
    ):
        ModelRequest(
            prompt="Hello Dobby",
            max_tokens=0,
        )


def test_model_request_accepts_valid_values() -> None:
    request = ModelRequest(
        prompt="Hello Dobby",
        system_prompt="You are Dobby.",
        capabilities=frozenset(
            {ModelCapability.TEXT_GENERATION}
        ),
        temperature=0.5,
        max_tokens=100,
        metadata={"source": "test"},
    )

    assert request.prompt == "Hello Dobby"
    assert request.system_prompt == "You are Dobby."
    assert ModelCapability.TEXT_GENERATION in request.capabilities
    assert request.temperature == 0.5
    assert request.max_tokens == 100
    assert request.metadata["source"] == "test"


def test_model_response_contains_runtime_identity() -> None:
    response = ModelResponse(
        text="Hello.",
        model_name="fake-model",
        runtime_name="fake-runtime",
    )

    assert response.text == "Hello."
    assert response.model_name == "fake-model"
    assert response.runtime_name == "fake-runtime"
