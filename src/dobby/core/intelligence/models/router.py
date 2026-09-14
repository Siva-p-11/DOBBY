from __future__ import annotations

from dataclasses import dataclass

from .model import Model, ModelCapability
from .registry import ModelRegistry
from .requirements import (
    ModelLatency,
    ModelModality,
    ModelRequirements,
)
from .specification import ModelSpecification


@dataclass(frozen=True)
class ModelRoutingDecision:
    """Represent the model selected for a workload."""

    model: Model
    specification: ModelSpecification
    requirements: ModelRequirements
    score: float


class ModelRouter:
    """Select an appropriate registered model for a workload."""

    def route(
        self,
        requirements: ModelRequirements,
        models: list[Model],
        specifications: dict[str, ModelSpecification],
    ) -> ModelRoutingDecision | None:
        """Select the best compatible model."""

        candidates: list[ModelRoutingDecision] = []

        for model in models:
            specification = specifications.get(model.name)

            if specification is None:
                continue

            if not self._supports_requirements(
                model,
                specification,
                requirements,
            ):
                continue

            score = self._score(
                model,
                specification,
                requirements,
            )

            candidates.append(
                ModelRoutingDecision(
                    model=model,
                    specification=specification,
                    requirements=requirements,
                    score=score,
                )
            )

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda decision: decision.score,
        )

    def _supports_requirements(
        self,
        model: Model,
        specification: ModelSpecification,
        requirements: ModelRequirements,
    ) -> bool:
        """Return whether a model satisfies workload requirements."""

        for capability in requirements.capabilities:
            if not model.supports(capability):
                return False

            if not specification.supports(capability):
                return False

        if (
            requirements.context_size is not None
            and specification.context_size is not None
            and specification.context_size < requirements.context_size
        ):
            return False

        if not self._supports_modality(
            specification,
            requirements,
        ):
            return False

        return True

    def _supports_modality(
        self,
        specification: ModelSpecification,
        requirements: ModelRequirements,
    ) -> bool:
        """Return whether the model supports the requested modality."""

        if requirements.modality == ModelModality.TEXT:
            return True

        if requirements.modality == ModelModality.VISION:
            return specification.supports(
                ModelCapability.VISION
            )

        if requirements.modality == ModelModality.AUDIO:
            return specification.supports(
                ModelCapability.AUDIO
            )

        if requirements.modality == ModelModality.MULTIMODAL:
            return (
                specification.supports(
                    ModelCapability.VISION
                )
                and specification.supports(
                    ModelCapability.AUDIO
                )
                and specification.supports(
                    ModelCapability.TEXT_GENERATION
                )
            )

        return False

    def _score(
        self,
        model: Model,
        specification: ModelSpecification,
        requirements: ModelRequirements,
    ) -> float:
        """Score a compatible model for the workload."""

        score = 100.0

        matched_capabilities = sum(
            1
            for capability in requirements.capabilities
            if model.supports(capability)
            and specification.supports(capability)
        )

        score += matched_capabilities * 10.0

        if (
            requirements.context_size is not None
            and specification.context_size is not None
            and specification.context_size > requirements.context_size
        ):
            score += 5.0

        if requirements.latency == ModelLatency.REALTIME:
            if "low_latency" in specification.runtime_requirements:
                score += 10.0

        if requirements.continuous:
            if "continuous" in specification.runtime_requirements:
                score += 5.0

        if requirements.parallel:
            if "parallel" in specification.runtime_requirements:
                score += 5.0

        if requirements.intensity.value == "high":
            if "high_performance" in specification.runtime_requirements:
                score += 10.0

        return score


class RegisteredModelRouter:
    """Route models using a ModelRegistry and stored specifications."""

    def __init__(
        self,
        registry: ModelRegistry,
        specifications: dict[str, ModelSpecification] | None = None,
        router: ModelRouter | None = None,
    ) -> None:
        self._registry = registry
        self._specifications = dict(specifications or {})
        self._router = router or ModelRouter()

    @property
    def specifications(self) -> dict[str, ModelSpecification]:
        """Return registered model specifications."""

        return dict(self._specifications)

    def register_specification(
        self,
        specification: ModelSpecification,
    ) -> None:
        """Register a specification for a model."""

        self._specifications[specification.name] = specification

    def route(
        self,
        requirements: ModelRequirements,
    ) -> ModelRoutingDecision | None:
        """Route a workload using the registry's models."""

        return self._router.route(
            requirements=requirements,
            models=list(self._registry.models),
            specifications=self._specifications,
        )
