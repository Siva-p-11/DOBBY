from __future__ import annotations

from dataclasses import dataclass

from .requirements import ComputeRequirements
from .resource import (
    ComputeCapability,
    ComputeResource,
    ComputeResourceType,
)
from .state import ComputeResourceStateSnapshot


@dataclass(frozen=True)
class ComputeSchedulingDecision:
    resource: ComputeResource
    requirements: ComputeRequirements
    state: ComputeResourceStateSnapshot
    score: float


class ComputeScheduler:
    """Select an appropriate compute resource for a workload."""

    def select(
        self,
        requirements: ComputeRequirements,
        resources: list[ComputeResource],
        states: dict[str, ComputeResourceStateSnapshot],
    ) -> ComputeSchedulingDecision | None:
        """Select the best currently usable resource."""

        candidates: list[ComputeSchedulingDecision] = []

        for resource in resources:
            if not resource.is_available():
                continue

            state = states.get(resource.name)

            if state is None:
                continue

            if not self._meets_memory_requirement(requirements, state):
                continue

            if not self._supports_requirements(resource, requirements):
                continue

            score = self._score(resource, requirements, state)

            candidates.append(
                ComputeSchedulingDecision(
                    resource=resource,
                    requirements=requirements,
                    state=state,
                    score=score,
                )
            )

        if not candidates:
            return None

        return max(candidates, key=lambda decision: decision.score)

    def _meets_memory_requirement(
        self,
        requirements: ComputeRequirements,
        state: ComputeResourceStateSnapshot,
    ) -> bool:
        """Check whether enough memory is available."""

        if requirements.memory_required_mb is None:
            return True

        if state.memory_available_mb is None:
            return True

        return state.memory_available_mb >= requirements.memory_required_mb

    def _supports_requirements(
        self,
        resource: ComputeResource,
        requirements: ComputeRequirements,
    ) -> bool:
        """Check whether a resource supports all required capabilities."""

        return all(
            resource.supports(capability)
            for capability in requirements.capabilities
        )

    def _score(
        self,
        resource: ComputeResource,
        requirements: ComputeRequirements,
        state: ComputeResourceStateSnapshot,
    ) -> float:
        """Calculate a preliminary suitability score."""

        score = 100.0

        score -= state.utilization_percent * 0.5

        if state.active_user_workload:
            score -= 50.0

        if requirements.intensity.value == "high":
            if resource.resource_type == ComputeResourceType.GPU:
                score += 30.0

        if requirements.continuous:
            if resource.resource_type == ComputeResourceType.NPU:
                score += 25.0

        if requirements.parallel:
            if resource.supports(ComputeCapability.PARALLEL_COMPUTE):
                score += 20.0

        if requirements.latency.value == "realtime":
            if resource.supports(ComputeCapability.LOW_LATENCY):
                score += 20.0

        return score
