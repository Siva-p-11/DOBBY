from __future__ import annotations

import pytest

from dobby.core.intelligence.models.model import (
    Model,
    ModelCapability,
)
from dobby.core.intelligence.models.registry import ModelRegistry
from dobby.core.intelligence.models.requirements import (
    ModelIntensity,
    ModelLatency,
    ModelModality,
    ModelRequirements,
)
from dobby.core.intelligence.models.router import (
    ModelRouter,
    RegisteredModelRouter,
)
from dobby.core.intelligence.models.specification import (
    ModelArchitecture,
    ModelSpecification,
)


class FakeModel(Model):
    """Minimal model implementation for router tests."""

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


def make_specification(
    name: str,
    capabilities: frozenset[ModelCapability],
    *,
    context_size: int | None = None,
    runtime_requirements: frozenset[str] = frozenset(),
) -> ModelSpecification:
    return ModelSpecification(
        name=name,
        version="1.0.0",
        architecture=ModelArchitecture.TRANSFORMER,
        capabilities=capabilities,
        context_size=context_size,
        runtime_requirements=runtime_requirements,
    )


def test_router_selects_compatible_model() -> None:
    model = FakeModel(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    specification = make_specification(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    router = ModelRouter()

    requirements = ModelRequirements(
        capabilities=frozenset({ModelCapability.CODING}),
        modality=ModelModality.TEXT,
    )

    decision = router.route(
        requirements=requirements,
        models=[model],
        specifications={"coding-model": specification},
    )

    assert decision is not None
    assert decision.model is model
    assert decision.specification is specification


def test_router_returns_none_when_no_model_is_compatible() -> None:
    model = FakeModel(
        "text-model",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    specification = make_specification(
        "text-model",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    router = ModelRouter()

    requirements = ModelRequirements(
        capabilities=frozenset({ModelCapability.CODING}),
    )

    decision = router.route(
        requirements=requirements,
        models=[model],
        specifications={"text-model": specification},
    )

    assert decision is None


def test_router_ignores_model_without_specification() -> None:
    model = FakeModel(
        "unregistered-spec",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    router = ModelRouter()

    requirements = ModelRequirements(
        capabilities=frozenset({ModelCapability.TEXT_GENERATION}),
    )

    decision = router.route(
        requirements=requirements,
        models=[model],
        specifications={},
    )

    assert decision is None


def test_router_rejects_insufficient_context_size() -> None:
    model = FakeModel(
        "small-context",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    specification = make_specification(
        "small-context",
        frozenset({ModelCapability.TEXT_GENERATION}),
        context_size=4096,
    )

    router = ModelRouter()

    requirements = ModelRequirements(
        capabilities=frozenset({ModelCapability.TEXT_GENERATION}),
        context_size=8192,
    )

    decision = router.route(
        requirements=requirements,
        models=[model],
        specifications={"small-context": specification},
    )

    assert decision is None


def test_router_accepts_sufficient_context_size() -> None:
    model = FakeModel(
        "large-context",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    specification = make_specification(
        "large-context",
        frozenset({ModelCapability.TEXT_GENERATION}),
        context_size=32768,
    )

    router = ModelRouter()

    requirements = ModelRequirements(
        capabilities=frozenset({ModelCapability.TEXT_GENERATION}),
        context_size=8192,
    )

    decision = router.route(
        requirements=requirements,
        models=[model],
        specifications={"large-context": specification},
    )

    assert decision is not None


def test_router_rejects_incompatible_vision_modality() -> None:
    model = FakeModel(
        "text-model",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    specification = make_specification(
        "text-model",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    router = ModelRouter()

    requirements = ModelRequirements(
        modality=ModelModality.VISION,
    )

    decision = router.route(
        requirements=requirements,
        models=[model],
        specifications={"text-model": specification},
    )

    assert decision is None


def test_router_accepts_vision_modality() -> None:
    model = FakeModel(
        "vision-model",
        frozenset(
            {
                ModelCapability.TEXT_GENERATION,
                ModelCapability.VISION,
            }
        ),
    )

    specification = make_specification(
        "vision-model",
        frozenset(
            {
                ModelCapability.TEXT_GENERATION,
                ModelCapability.VISION,
            }
        ),
    )

    router = ModelRouter()

    requirements = ModelRequirements(
        modality=ModelModality.VISION,
    )

    decision = router.route(
        requirements=requirements,
        models=[model],
        specifications={"vision-model": specification},
    )

    assert decision is not None
    assert decision.model is model


def test_router_scores_capability_matches() -> None:
    model = FakeModel(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    specification = make_specification(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    router = ModelRouter()

    requirements = ModelRequirements(
        capabilities=frozenset({ModelCapability.CODING}),
    )

    decision = router.route(
        requirements=requirements,
        models=[model],
        specifications={"coding-model": specification},
    )

    assert decision is not None
    assert decision.score >= 110.0


def test_router_prefers_better_scoring_model() -> None:
    basic_model = FakeModel(
        "basic-model",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    optimized_model = FakeModel(
        "optimized-model",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    basic_specification = make_specification(
        "basic-model",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    optimized_specification = make_specification(
        "optimized-model",
        frozenset({ModelCapability.TEXT_GENERATION}),
        runtime_requirements=frozenset(
            {
                "low_latency",
                "continuous",
                "parallel",
                "high_performance",
            }
        ),
    )

    router = ModelRouter()

    requirements = ModelRequirements(
        capabilities=frozenset({ModelCapability.TEXT_GENERATION}),
        intensity=ModelIntensity.HIGH,
        latency=ModelLatency.REALTIME,
        continuous=True,
        parallel=True,
    )

    decision = router.route(
        requirements=requirements,
        models=[
            basic_model,
            optimized_model,
        ],
        specifications={
            "basic-model": basic_specification,
            "optimized-model": optimized_specification,
        },
    )

    assert decision is not None
    assert decision.model is optimized_model


def test_registered_router_uses_registry_models() -> None:
    registry = ModelRegistry()

    model = FakeModel(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    registry.register(model)

    specification = make_specification(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    router = RegisteredModelRouter(
        registry=registry,
        specifications={
            "coding-model": specification,
        },
    )

    requirements = ModelRequirements(
        capabilities=frozenset({ModelCapability.CODING}),
    )

    decision = router.route(requirements)

    assert decision is not None
    assert decision.model is model


def test_registered_router_can_register_specification() -> None:
    registry = ModelRegistry()

    model = FakeModel(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    registry.register(model)

    router = RegisteredModelRouter(registry)

    specification = make_specification(
        "coding-model",
        frozenset({ModelCapability.CODING}),
    )

    router.register_specification(specification)

    assert router.specifications["coding-model"] is specification


def test_registered_router_returns_none_without_compatible_model() -> None:
    registry = ModelRegistry()

    model = FakeModel(
        "text-model",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    registry.register(model)

    specification = make_specification(
        "text-model",
        frozenset({ModelCapability.TEXT_GENERATION}),
    )

    router = RegisteredModelRouter(
        registry=registry,
        specifications={
            "text-model": specification,
        },
    )

    requirements = ModelRequirements(
        capabilities=frozenset({ModelCapability.CODING}),
    )

    assert router.route(requirements) is None
