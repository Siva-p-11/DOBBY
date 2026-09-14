from __future__ import annotations

from .allocation import ComputeAllocation
from .budget import ComputeBudget
from .priority import ComputePriorityRequest
from .requirements import ComputeRequirements
from .resource import ComputeResource
from .scheduler import ComputeScheduler
from .state import ComputeResourceStateSnapshot


class ComputeManager:
    """Coordinate compute resources, scheduling, and allocations."""

    def __init__(
        self,
        resources: list[ComputeResource] | None = None,
        scheduler: ComputeScheduler | None = None,
    ) -> None:
        self._resources = list(resources or [])
        self._scheduler = scheduler or ComputeScheduler()
        self._states: dict[str, ComputeResourceStateSnapshot] = {}
        self._allocations: dict[str, ComputeAllocation] = {}

    @property
    def resources(self) -> tuple[ComputeResource, ...]:
        """Return registered compute resources."""

        return tuple(self._resources)

    @property
    def allocations(self) -> tuple[ComputeAllocation, ...]:
        """Return current allocation records."""

        return tuple(self._allocations.values())

    def register_resource(
        self,
        resource: ComputeResource,
        state: ComputeResourceStateSnapshot | None = None,
    ) -> None:
        """Register a compute resource and optionally its current state."""

        if any(existing.name == resource.name for existing in self._resources):
            raise ValueError(
                f"Compute resource already registered: {resource.name}"
            )

        self._resources.append(resource)

        if state is not None:
            self._states[resource.name] = state

    def update_state(
        self,
        resource_name: str,
        state: ComputeResourceStateSnapshot,
    ) -> None:
        """Update the latest known state of a resource."""

        if not any(
            resource.name == resource_name
            for resource in self._resources
        ):
            raise KeyError(f"Unknown compute resource: {resource_name}")

        self._states[resource_name] = state

    def get_state(
        self,
        resource_name: str,
    ) -> ComputeResourceStateSnapshot | None:
        """Return the latest known state of a resource."""

        return self._states.get(resource_name)

    def request_allocation(
        self,
        workload_id: str,
        requirements: ComputeRequirements,
        budget: ComputeBudget,
        priority: ComputePriorityRequest,
    ) -> ComputeAllocation | None:
        """Request compute allocation for a workload."""

        if workload_id in self._allocations:
            raise ValueError(
                f"Allocation already exists: {workload_id}"
            )

        decision = self._scheduler.select(
            requirements=requirements,
            resources=self._resources,
            states=self._states,
        )

        if decision is None:
            return None

        allocation = ComputeAllocation(
            workload_id=workload_id,
            resource=decision.resource,
            requirements=requirements,
            budget=budget,
            priority=priority,
            resource_state=decision.state,
        )

        self._allocations[workload_id] = allocation

        return allocation

    def approve_allocation(
        self,
        workload_id: str,
    ) -> ComputeAllocation:
        """Mark an existing allocation as approved."""

        allocation = self._get_allocation(workload_id)
        updated = allocation.approve()

        self._allocations[workload_id] = updated

        return updated

    def activate_allocation(
        self,
        workload_id: str,
    ) -> ComputeAllocation:
        """Mark an existing allocation as active."""

        allocation = self._get_allocation(workload_id)
        updated = allocation.activate()

        self._allocations[workload_id] = updated

        return updated

    def release_allocation(
        self,
        workload_id: str,
    ) -> ComputeAllocation:
        """Release an existing allocation."""

        allocation = self._get_allocation(workload_id)
        updated = allocation.release()

        self._allocations[workload_id] = updated

        return updated

    def reject_allocation(
        self,
        workload_id: str,
    ) -> ComputeAllocation:
        """Reject an existing allocation."""

        allocation = self._get_allocation(workload_id)
        updated = allocation.reject()

        self._allocations[workload_id] = updated

        return updated

    def remove_allocation(self, workload_id: str) -> None:
        """Remove an allocation record."""

        if workload_id not in self._allocations:
            raise KeyError(f"Unknown allocation: {workload_id}")

        del self._allocations[workload_id]

    def _get_allocation(
        self,
        workload_id: str,
    ) -> ComputeAllocation:
        """Return an allocation or raise if it does not exist."""

        try:
            return self._allocations[workload_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown allocation: {workload_id}"
            ) from exc
