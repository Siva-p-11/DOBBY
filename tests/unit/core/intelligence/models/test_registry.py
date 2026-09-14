from __future__ import annotations

import pytest

from dobby.core.intelligence.models.model import (
    Model,
    ModelCapability,
)
from dobby.core.intelligence.models.registry import ModelRegistry


class FakeModel(Model):
    """Minimal model implementation for registry tests."""

    def __init__(
        self,
        name: str,
        capabilities: frozenset[ModelCapability],
    ) -> None:
        self._name = name
        self._capabilities = capabilities

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> frozenset[ModelCapability]:
        return self._capabilities


def test_registry_starts_empty() -> None:
    registry = ModelRegistry()

    assert registry.models == ()


def test_registry_registers_model() -> None:
    registry = ModelRegistry()
    model = FakeModel(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    registry.register(model)

    assert registry.get("coding-model") is model
    assert registry.models == (model,)


def test_registry_rejects_duplicate_model() -> None:
    registry = ModelRegistry()
    model = FakeModel(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    registry.register(model)

    with pytest.raises(
        ValueError,
        match="Model already registered",
    ):
        registry.register(model)


def test_registry_get_rejects_unknown_model() -> None:
    registry = ModelRegistry()

    with pytest.raises(
        KeyError,
        match="Unknown model",
    ):
        registry.get("missing-model")


def test_registry_unregisters_model() -> None:
    registry = ModelRegistry()
    model = FakeModel(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    registry.register(model)
    registry.unregister("coding-model")

    assert registry.models == ()


def test_registry_unregister_rejects_unknown_model() -> None:
    registry = ModelRegistry()

    with pytest.raises(
        KeyError,
        match="Unknown model",
    ):
        registry.unregister("missing-model")


def test_registry_finds_models_by_capability() -> None:
    registry = ModelRegistry()

    coding_model = FakeModel(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    reasoning_model = FakeModel(
        "reasoning-model",
        frozenset({ModelCapability.REASONING}),
    )

    hybrid_model = FakeModel(
        "hybrid-model",
        frozenset(
            {
                ModelCapability.CODING,
                ModelCapability.REASONING,
            }
        ),
    )

    registry.register(coding_model)
    registry.register(reasoning_model)
    registry.register(hybrid_model)

    coding_models = registry.find_by_capability(
        ModelCapability.CODING
    )

    assert coding_models == (
        coding_model,
        hybrid_model,
    )


def test_registry_returns_empty_for_unsupported_capability() -> None:
    registry = ModelRegistry()

    registry.register(
        FakeModel(
            "coding-model",
            frozenset({ModelCapability.CODING}),
        )
    )

    assert registry.find_by_capability(
        ModelCapability.VISION
    ) == ()
