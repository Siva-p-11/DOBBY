from __future__ import annotations

import pytest

from dobby.core.intelligence.models.model import (
    Model,
    ModelCapability,
    ModelRequest,
    ModelResponse,
)
from dobby.core.intelligence.models.runtime import ModelRuntime


class FakeModel(Model):
    """Minimal model implementation for runtime contract tests."""

    @property
    def name(self) -> str:
        return "fake-model"

    @property
    def capabilities(self) -> frozenset[ModelCapability]:
        return frozenset({ModelCapability.TEXT_GENERATION})


class FakeRuntime(ModelRuntime):
    """Minimal runtime implementation for contract tests."""

    def __init__(self) -> None:
        self.loaded_models: set[str] = set()

    @property
    def name(self) -> str:
        return "fake-runtime"

    def load(self, model: Model) -> None:
        self.loaded_models.add(model.name)

    def unload(self, model: Model) -> None:
        self.loaded_models.discard(model.name)

    def is_loaded(self, model: Model) -> bool:
        return model.name in self.loaded_models

    def generate(
        self,
        model: Model,
        request: ModelRequest,
    ) -> ModelResponse:
        if not self.is_loaded(model):
            raise RuntimeError(
                f"Model is not loaded: {model.name}"
            )

        return ModelResponse(
            text=f"Generated response for: {request.prompt}",
            model_name=model.name,
            runtime_name=self.name,
        )


def test_runtime_has_name() -> None:
    runtime = FakeRuntime()

    assert runtime.name == "fake-runtime"


def test_runtime_can_load_model() -> None:
    runtime = FakeRuntime()
    model = FakeModel()

    runtime.load(model)

    assert runtime.is_loaded(model)


def test_runtime_can_unload_model() -> None:
    runtime = FakeRuntime()
    model = FakeModel()

    runtime.load(model)
    runtime.unload(model)

    assert not runtime.is_loaded(model)


def test_runtime_rejects_generation_for_unloaded_model() -> None:
    runtime = FakeRuntime()
    model = FakeModel()
    request = ModelRequest(prompt="Hello Dobby")

    with pytest.raises(RuntimeError, match="Model is not loaded"):
        runtime.generate(model, request)


def test_runtime_generates_response_for_loaded_model() -> None:
    runtime = FakeRuntime()
    model = FakeModel()
    request = ModelRequest(prompt="Hello Dobby")

    runtime.load(model)

    response = runtime.generate(model, request)

    assert response.text == "Generated response for: Hello Dobby"
    assert response.model_name == "fake-model"
    assert response.runtime_name == "fake-runtime"
