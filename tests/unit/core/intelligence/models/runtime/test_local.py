from __future__ import annotations

from typing import FrozenSet

import pytest

from dobby.core.intelligence.models.model import (
    Model,
    ModelCapability,
    ModelRequest,
    ModelResponse,
)
from dobby.core.intelligence.models.runtime.backend import (
    ModelExecutionBackend,
)
from dobby.core.intelligence.models.runtime.local import LocalModelRuntime


class FakeModel(Model):
    @property
    def name(self) -> str:
        return "test-model"

    @property
    def capabilities(self) -> FrozenSet[ModelCapability]:
        return frozenset({ModelCapability.TEXT_GENERATION})


class FakeBackend(ModelExecutionBackend):
    def __init__(
        self,
        name: str = "fake-backend",
        capabilities: FrozenSet[str] | None = None,
    ) -> None:
        self._name = name
        self._capabilities = capabilities or frozenset()
        self._loaded: set[str] = set()
        self.load_calls = 0
        self.unload_calls = 0
        self.generate_calls = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> FrozenSet[str]:
        return self._capabilities

    def load(self, model: Model) -> None:
        self.load_calls += 1
        self._loaded.add(model.name)

    def unload(self, model: Model) -> None:
        self.unload_calls += 1
        self._loaded.discard(model.name)

    def is_loaded(self, model: Model) -> bool:
        return model.name in self._loaded

    def generate(
        self,
        model: Model,
        request: ModelRequest,
    ) -> ModelResponse:
        self.generate_calls += 1

        return ModelResponse(
            text=f"Generated response for: {request.prompt}",
            model_name=model.name,
            runtime_name="local:fake-backend",
            input_tokens=1,
            output_tokens=2,
        )


def test_local_runtime_uses_backend_name() -> None:
    backend = FakeBackend(name="test-backend")

    runtime = LocalModelRuntime(backend)

    assert runtime.name == "local:test-backend"


def test_local_runtime_exposes_backend_capabilities() -> None:
    backend = FakeBackend(
        capabilities=frozenset({"cuda", "gpu"})
    )

    runtime = LocalModelRuntime(backend)

    assert runtime.capabilities == frozenset({"cuda", "gpu"})
    assert runtime.supports("cuda") is True
    assert runtime.supports("gpu") is True
    assert runtime.supports("npu") is False


def test_local_runtime_loads_model_through_backend() -> None:
    backend = FakeBackend()
    runtime = LocalModelRuntime(backend)
    model = FakeModel()

    runtime.load(model)

    assert backend.load_calls == 1
    assert runtime.is_loaded(model) is True


def test_local_runtime_unloads_model_through_backend() -> None:
    backend = FakeBackend()
    runtime = LocalModelRuntime(backend)
    model = FakeModel()

    runtime.load(model)
    runtime.unload(model)

    assert backend.load_calls == 1
    assert backend.unload_calls == 1
    assert runtime.is_loaded(model) is False


def test_local_runtime_generates_through_backend() -> None:
    backend = FakeBackend()
    runtime = LocalModelRuntime(backend)
    model = FakeModel()

    runtime.load(model)

    request = ModelRequest(
        prompt="Hello Dobby",
    )

    response = runtime.generate(
        model,
        request,
    )

    assert backend.generate_calls == 1
    assert response.text == "Generated response for: Hello Dobby"
    assert response.model_name == "test-model"
    assert response.runtime_name == "local:fake-backend"


def test_local_runtime_rejects_generation_when_model_not_loaded() -> None:
    backend = FakeBackend()
    runtime = LocalModelRuntime(backend)
    model = FakeModel()

    request = ModelRequest(
        prompt="Hello Dobby",
    )

    with pytest.raises(
        RuntimeError,
        match="Model is not loaded",
    ):
        runtime.generate(
            model,
            request,
        )

    assert backend.generate_calls == 0


def test_local_runtime_propagates_backend_load_error() -> None:
    class FailingBackend(FakeBackend):
        def load(self, model: Model) -> None:
            raise RuntimeError("backend load failed")

    backend = FailingBackend()
    runtime = LocalModelRuntime(backend)
    model = FakeModel()

    with pytest.raises(
        RuntimeError,
        match="backend load failed",
    ):
        runtime.load(model)


def test_local_runtime_propagates_backend_unload_error() -> None:
    class FailingBackend(FakeBackend):
        def unload(self, model: Model) -> None:
            raise RuntimeError("backend unload failed")

    backend = FailingBackend()
    runtime = LocalModelRuntime(backend)
    model = FakeModel()

    runtime.load(model)

    with pytest.raises(
        RuntimeError,
        match="backend unload failed",
    ):
        runtime.unload(model)

    assert runtime.is_loaded(model) is True


def test_local_runtime_propagates_backend_generate_error() -> None:
    class FailingBackend(FakeBackend):
        def generate(
            self,
            model: Model,
            request: ModelRequest,
        ) -> ModelResponse:
            raise RuntimeError("backend generation failed")

    backend = FailingBackend()
    runtime = LocalModelRuntime(backend)
    model = FakeModel()

    runtime.load(model)

    request = ModelRequest(
        prompt="Hello Dobby",
    )

    with pytest.raises(
        RuntimeError,
        match="backend generation failed",
    ):
        runtime.generate(
            model,
            request,
        )
