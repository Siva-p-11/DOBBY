from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class ComputePriority(IntEnum):
    """Priority levels for compute workloads."""

    BACKGROUND = 10
    NORMAL = 30
    INTERACTIVE = 60
    USER_RESERVED = 90
    CRITICAL = 100


@dataclass(frozen=True)
class ComputePriorityRequest:
    """Describe the priority assigned to a compute workload."""

    priority: ComputePriority = ComputePriority.NORMAL
    reason: str = ""

    def is_higher_than(
        self,
        other: ComputePriorityRequest,
    ) -> bool:
        """Return whether this request has higher priority."""

        return self.priority > other.priority

    def is_user_priority(self) -> bool:
        """Return whether this workload has user-level priority."""

        return self.priority == ComputePriority.USER_RESERVED

    def is_interactive(self) -> bool:
        """Return whether this workload requires interactive priority."""

        return self.priority == ComputePriority.INTERACTIVE
