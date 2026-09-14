from __future__ import annotations

from typing import FrozenSet

import pytest

from dobby.core.intelligence.models.model import (
    Model,
    ModelCapability,
    ModelRequest,
    ModelResponse,
)
from dobby.core.intelligence.models.runtime.runtime import ModelRuntime
from dobby.core.intelligence.models.runtime.selection import (
    RuntimeRequirements,
)
from dobby.core.intelligence.models.runtime.selector import RuntimeSelector


class FakeModel(Model):
    @property
    def name(self) -> str:
        return "fake-model"

    @property
    def capabilities(self) -> FrozenSet[ModelCapability]:
        return frozenset({ModelCapability.TEXT_GENERATION})


class FakeRuntime(ModelRuntime):
    def __init__(
        self,
        runtime_name: str,
        runtime_capabilities: set[str],
    ) -> None:
        self._name = runtime_name
        self._capabilities = frozenset(runtime_capabilities)
        self.loaded_models: set[str] = set()

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> FrozenSet[str]:
        return self._capabilities

    def supports(self, requirement: str) -> bool:
        return requirement in self.capabilities

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
        return ModelResponse(
            text="fake response",
            model_name=model.name,
            runtime_name=self.name,
        )


def test_selector_selects_compatible_runtime() -> None:
    selector = RuntimeSelector()

    cpu = FakeRuntime(
        "cpu",
        {"cpu"},
    )
    cuda = FakeRuntime(
        "cuda",
        {"cuda", "gpu"},
    )

    requirements = RuntimeRequirements(
        frozenset({"cuda"}),
    )

    decision = selector.select(
        requirements,
        [cpu, cuda],
    )

    assert decision is not None
    assert decision.runtime.name == "cuda"


def test_selector_rejects_incompatible_runtime() -> None:
    selector = RuntimeSelector()

    cpu = FakeRuntime(
        "cpu",
        {"cpu"},
    )

    requirements = RuntimeRequirements(
        frozenset({"cuda"}),
    )

    decision = selector.select(
        requirements,
        [cpu],
    )

    assert decision is None


def test_selector_returns_none_when_no_runtimes_exist() -> None:
    selector = RuntimeSelector()

    requirements = RuntimeRequirements(
        frozenset({"cuda"}),
    )

    decision = selector.select(
        requirements,
        [],
    )

    assert decision is None


def test_selector_requires_all_runtime_requirements() -> None:
    selector = RuntimeSelector()

    partial = FakeRuntime(
        "partial",
        {"cuda"},
    )

    complete = FakeRuntime(
        "complete",
        {"cuda", "gpu"},
    )

    requirements = RuntimeRequirements(
        frozenset({"cuda", "gpu"}),
    )

    decision = selector.select(
        requirements,
        [partial, complete],
    )

    assert decision is not None
    assert decision.runtime.name == "complete"


def test_selector_does_not_reward_unrequested_capabilities() -> None:
    selector = RuntimeSelector()

    basic = FakeRuntime(
        "basic",
        {"cuda"},
    )

    advanced = FakeRuntime(
        "advanced",
        {"cuda", "gpu", "tensor_cores"},
    )

    requirements = RuntimeRequirements(
        frozenset({"cuda"}),
    )

    decision = selector.select(
        requirements,
        [basic, advanced],
    )

    assert decision is not None
    assert decision.runtime.name == "basic"


def test_runtime_requirements_detect_required_feature() -> None:
    requirements = RuntimeRequirements(
        frozenset({"cuda", "gpu"}),
    )

    assert requirements.requires("cuda")
    assert requirements.requires("gpu")
    assert not requirements.requires("cpu")


def test_empty_requirements_allow_any_runtime() -> None:
    selector = RuntimeSelector()

    cpu = FakeRuntime(
        "cpu",
        {"cpu"},
    )

    cuda = FakeRuntime(
        "cuda",
        {"cuda"},
    )

    requirements = RuntimeRequirements()

    decision = selector.select(
        requirements,
        [cpu, cuda],
    )

    assert decision is not None
    assert decision.runtime.name == "cpu"
