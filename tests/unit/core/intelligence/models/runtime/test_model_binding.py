from __future__ import annotations

from typing import FrozenSet

from dobby.core.intelligence.models.model import (
    Model,
    ModelCapability,
)
from dobby.core.intelligence.models.runtime.binding import ModelBinding
from dobby.core.intelligence.models.specification import (
    ModelSpecification,
)


class FakeModel(Model):
    def __init__(
        self,
        name: str = "test-model",
        capabilities: FrozenSet[ModelCapability] | None = None,
    ) -> None:
        self._name = name
        self._capabilities = capabilities or frozenset(
            {ModelCapability.TEXT_GENERATION}
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> FrozenSet[ModelCapability]:
        return self._capabilities


def test_binding_matches_model_and_specification() -> None:
    model = FakeModel()

    specification = ModelSpecification(
        name="test-model",
        version="1.0",
        capabilities=frozenset({ModelCapability.TEXT_GENERATION}),
    )

    binding = ModelBinding(
        model=model,
        specification=specification,
    )

    assert binding.matches() is True


def test_binding_rejects_different_model_name() -> None:
    model = FakeModel(name="model-a")

    specification = ModelSpecification(
        name="model-b",
        version="1.0",
        capabilities=frozenset({ModelCapability.TEXT_GENERATION}),
    )

    binding = ModelBinding(
        model=model,
        specification=specification,
    )

    assert binding.matches() is False


def test_binding_rejects_unsupported_specification_capability() -> None:
    model = FakeModel(
        capabilities=frozenset({ModelCapability.TEXT_GENERATION})
    )

    specification = ModelSpecification(
        name="test-model",
        version="1.0",
        capabilities=frozenset(
            {
                ModelCapability.TEXT_GENERATION,
                ModelCapability.VISION,
            }
        ),
    )

    binding = ModelBinding(
        model=model,
        specification=specification,
    )

    assert binding.matches() is False


def test_binding_accepts_model_with_additional_capabilities() -> None:
    model = FakeModel(
        capabilities=frozenset(
            {
                ModelCapability.TEXT_GENERATION,
                ModelCapability.REASONING,
            }
        )
    )

    specification = ModelSpecification(
        name="test-model",
        version="1.0",
        capabilities=frozenset({ModelCapability.TEXT_GENERATION}),
    )

    binding = ModelBinding(
        model=model,
        specification=specification,
    )

    assert binding.matches() is True
