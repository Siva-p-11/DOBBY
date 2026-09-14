from __future__ import annotations

import pytest

from dobby.core.intelligence.models.model import (
    Model,
    ModelCapability,
    ModelRequest,
    ModelResponse,
)
from dobby.core.intelligence.models.runtime import (
    ManagedModel,
    ModelRuntime,
    ModelRuntimeState,
)


class FakeModel(Model):
    @property
    def name(self) -> str:
        return "fake-model"

    @property
    def capabilities(self) -> frozenset[ModelCapability]:
        return frozenset({ModelCapability.TEXT_GENERATION})


class FakeRuntime(ModelRuntime):
    def __init__(
        self,
        name: str = "fake-runtime",
        *,
        fail_load: bool = False,
        fail_unload: bool = False,
    ) -> None:
        self._name = name
        self.fail_load = fail_load
        self.fail_unload = fail_unload
        self.loaded_models: list[Model] = []

    @property
    def name(self) -> str:
        return self._name

    def load(self, model: Model) -> None:
        if self.fail_load:
            raise RuntimeError("load failed")

        self.loaded_models.append(model)

    def unload(self, model: Model) -> None:
        if self.fail_unload:
            raise RuntimeError("unload failed")

        if model in self.loaded_models:
            self.loaded_models.remove(model)

    def is_loaded(self, model: Model) -> bool:
        return model in self.loaded_models

    def generate(
        self,
        model: Model,
        request: ModelRequest,
    ) -> ModelResponse:
        return ModelResponse(
            text="fake response",
            model_name=model.name,
            runtime_name=self.name,
        )


def test_managed_model_starts_unloaded() -> None:
    model = FakeModel()
    runtime = FakeRuntime()

    managed = ManagedModel(
        model=model,
        runtime=runtime,
    )

    assert managed.state == ModelRuntimeState.UNLOADED
    assert not managed.is_loaded()


def test_managed_model_loads_model() -> None:
    model = FakeModel()
    runtime = FakeRuntime()

    managed = ManagedModel(
        model=model,
        runtime=runtime,
    )

    managed.load()

    assert managed.state == ModelRuntimeState.LOADED
    assert managed.is_loaded()
    assert runtime.is_loaded(model)


def test_managed_model_load_is_idempotent() -> None:
    model = FakeModel()
    runtime = FakeRuntime()

    managed = ManagedModel(
        model=model,
        runtime=runtime,
    )

    managed.load()
    managed.load()

    assert managed.state == ModelRuntimeState.LOADED
    assert runtime.loaded_models == [model]


def test_managed_model_unloads_model() -> None:
    model = FakeModel()
    runtime = FakeRuntime()

    managed = ManagedModel(
        model=model,
        runtime=runtime,
    )

    managed.load()
    managed.unload()

    assert managed.state == ModelRuntimeState.UNLOADED
    assert not managed.is_loaded()
    assert not runtime.is_loaded(model)


def test_managed_model_unload_is_idempotent() -> None:
    model = FakeModel()
    runtime = FakeRuntime()

    managed = ManagedModel(
        model=model,
        runtime=runtime,
    )

    managed.unload()

    assert managed.state == ModelRuntimeState.UNLOADED


def test_load_failure_restores_unloaded_state() -> None:
    model = FakeModel()
    runtime = FakeRuntime(fail_load=True)

    managed = ManagedModel(
        model=model,
        runtime=runtime,
    )

    with pytest.raises(
        RuntimeError,
        match="load failed",
    ):
        managed.load()

    assert managed.state == ModelRuntimeState.UNLOADED
    assert not managed.is_loaded()


def test_unload_failure_restores_loaded_state() -> None:
    model = FakeModel()
    runtime = FakeRuntime(fail_unload=True)

    managed = ManagedModel(
        model=model,
        runtime=runtime,
    )

    managed.load()

    with pytest.raises(
        RuntimeError,
        match="unload failed",
    ):
        managed.unload()

    assert managed.state == ModelRuntimeState.LOADED
    assert managed.is_loaded()


def test_loading_from_invalid_state_is_rejected() -> None:
    model = FakeModel()
    runtime = FakeRuntime()

    managed = ManagedModel(
        model=model,
        runtime=runtime,
        state=ModelRuntimeState.LOADING,
    )

    with pytest.raises(
        RuntimeError,
        match="Cannot load model from state: loading",
    ):
        managed.load()


def test_unloading_from_invalid_state_is_rejected() -> None:
    model = FakeModel()
    runtime = FakeRuntime()

    managed = ManagedModel(
        model=model,
        runtime=runtime,
        state=ModelRuntimeState.UNLOADING,
    )

    with pytest.raises(
        RuntimeError,
        match="Cannot unload model from state: unloading",
    ):
        managed.unload()
