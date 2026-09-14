from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .budget import ComputeBudget
from .priority import ComputePriorityRequest
from .requirements import ComputeRequirements
from .resource import ComputeResource
from .state import ComputeResourceStateSnapshot


class ComputeAllocationState(str, Enum):
    """State of a compute allocation."""

    REQUESTED = "requested"
    APPROVED = "approved"
    ACTIVE = "active"
    RELEASED = "released"
    REJECTED = "rejected"


@dataclass(frozen=True)
class ComputeAllocation:
    """Represent a compute allocation decision."""

    workload_id: str

    resource: ComputeResource
    requirements: ComputeRequirements
    budget: ComputeBudget
    priority: ComputePriorityRequest

    state: ComputeAllocationState = ComputeAllocationState.REQUESTED

    resource_state: ComputeResourceStateSnapshot | None = None

    def approve(self) -> ComputeAllocation:
        """Return a new allocation marked as approved."""

        return self._with_state(ComputeAllocationState.APPROVED)

    def activate(self) -> ComputeAllocation:
        """Return a new allocation marked as active."""

        return self._with_state(ComputeAllocationState.ACTIVE)

    def release(self) -> ComputeAllocation:
        """Return a new allocation marked as released."""

        return self._with_state(ComputeAllocationState.RELEASED)

    def reject(self) -> ComputeAllocation:
        """Return a new allocation marked as rejected."""

        return self._with_state(ComputeAllocationState.REJECTED)

    def _with_state(
        self,
        state: ComputeAllocationState,
    ) -> ComputeAllocation:
        """Return a copy with a different allocation state."""

        return ComputeAllocation(
            workload_id=self.workload_id,
            resource=self.resource,
            requirements=self.requirements,
            budget=self.budget,
            priority=self.priority,
            state=state,
            resource_state=self.resource_state,
        )
