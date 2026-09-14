from __future__ import annotations

from .runtime import ModelRuntime
from .selection import (
    RuntimeRequirements,
    RuntimeSelectionDecision,
)


class RuntimeSelector:
    """Select the most suitable runtime for a workload."""

    def select(
        self,
        requirements: RuntimeRequirements,
        runtimes: list[ModelRuntime],
    ) -> RuntimeSelectionDecision | None:
        """Select the best compatible runtime."""

        candidates: list[RuntimeSelectionDecision] = []

        for runtime in runtimes:
            if not self._supports_requirements(
                runtime,
                requirements,
            ):
                continue

            score = self._score(
                runtime,
                requirements,
            )

            candidates.append(
                RuntimeSelectionDecision(
                    runtime=runtime,
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
        runtime: ModelRuntime,
        requirements: RuntimeRequirements,
    ) -> bool:
        """Return whether a runtime satisfies the requirements."""

        return all(
            runtime.supports(requirement)
            for requirement in requirements.requirements
        )

    def _score(
        self,
        runtime: ModelRuntime,
        requirements: RuntimeRequirements,
    ) -> float:
        """Score a compatible runtime."""

        matched = sum(
            1
            for requirement in requirements.requirements
            if runtime.supports(requirement)
        )

        return 100.0 + matched * 10.0
