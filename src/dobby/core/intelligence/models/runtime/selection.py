from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet

from .runtime import ModelRuntime


@dataclass(frozen=True)
class RuntimeRequirements:
    """Describe the runtime features required by a workload."""

    requirements: FrozenSet[str] = field(default_factory=frozenset)

    def requires(self, requirement: str) -> bool:
        """Return whether a runtime requirement is required."""
        return requirement in self.requirements


@dataclass(frozen=True)
class RuntimeSelectionDecision:
    """Represent the runtime selected for a workload."""

    runtime: ModelRuntime
    score: float
