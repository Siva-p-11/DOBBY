from __future__ import annotations

import pytest

from dobby.core.intelligence.models.model import (
    Model,
    ModelCapability,
)
from dobby.core.intelligence.models.runtime import (
    ModelRuntime,
    ModelRuntimeManager,
)


class FakeModel(Model):
    @property
    def name(self) -> str:
        return "fake-model"

    @property
    def capabilities(self) -> frozenset[ModelCapability]:
        return frozenset({ModelCapability.TEXT_GENERATION})


class FakeRuntime(ModelRuntime):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def load(self, model: Model) -> None:
        pass

    def unload(self, model: Model) -> None:
        pass

    def is_loaded(self, model: Model) -> bool:
        return False

    def generate(self, model, request):
        raise NotImplementedError


def test_manager_starts_empty() -> None:
    manager = ModelRuntimeManager()

    assert manager.runtimes == ()


def test_manager_registers_runtime() -> None:
    manager = ModelRuntimeManager()
    runtime = FakeRuntime("fake-runtime")

    manager.register(runtime)

    assert manager.runtimes == (runtime,)
    assert manager.get("fake-runtime") is runtime


def test_manager_rejects_duplicate_runtime() -> None:
    manager = ModelRuntimeManager()
    runtime = FakeRuntime("fake-runtime")

    manager.register(runtime)

    with pytest.raises(
        ValueError,
        match="Runtime already registered: fake-runtime",
    ):
        manager.register(runtime)


def test_manager_unregisters_runtime() -> None:
    manager = ModelRuntimeManager()
    runtime = FakeRuntime("fake-runtime")

    manager.register(runtime)
    manager.unregister("fake-runtime")

    assert manager.runtimes == ()


def test_manager_rejects_unknown_runtime() -> None:
    manager = ModelRuntimeManager()

    with pytest.raises(
        KeyError,
        match="Unknown runtime: missing-runtime",
    ):
        manager.get("missing-runtime")


def test_manager_rejects_unregistering_unknown_runtime() -> None:
    manager = ModelRuntimeManager()

    with pytest.raises(
        KeyError,
        match="Unknown runtime: missing-runtime",
    ):
        manager.unregister("missing-runtime")
