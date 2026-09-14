import pytest

from dobby.core.compute.budget import ComputeBudget
from dobby.core.compute.manager import ComputeManager
from dobby.core.compute.priority import ComputePriorityRequest
from dobby.core.compute.requirements import ComputeRequirements
from dobby.core.compute.resource import (
    ComputeCapability,
    ComputeResource,
    ComputeResourceType,
)
from dobby.core.compute.state import ComputeResourceStateSnapshot


def make_cpu(name: str = "cpu") -> ComputeResource:
    return ComputeResource(
        name=name,
        resource_type=ComputeResourceType.CPU,
        architecture="x86_64",
        capabilities=frozenset(
            {
                ComputeCapability.GENERAL_COMPUTE,
                ComputeCapability.AI_INFERENCE,
            }
        ),
    )


def make_manager() -> ComputeManager:
    manager = ComputeManager()

    manager.register_resource(
        make_cpu(),
        ComputeResourceStateSnapshot(),
    )

    return manager


def test_manager_registers_resource() -> None:
    manager = ComputeManager()

    manager.register_resource(
        make_cpu(),
        ComputeResourceStateSnapshot(),
    )

    assert len(manager.resources) == 1
    assert manager.resources[0].name == "cpu"


def test_manager_rejects_duplicate_resource() -> None:
    manager = make_manager()

    with pytest.raises(ValueError):
        manager.register_resource(make_cpu())


def test_manager_updates_resource_state() -> None:
    manager = make_manager()

    state = ComputeResourceStateSnapshot(
        utilization_percent=75.0,
    )

    manager.update_state("cpu", state)

    assert manager.get_state("cpu") == state


def test_manager_rejects_unknown_resource_state() -> None:
    manager = make_manager()

    with pytest.raises(KeyError):
        manager.update_state(
            "unknown",
            ComputeResourceStateSnapshot(),
        )


def test_manager_creates_allocation() -> None:
    manager = make_manager()

    allocation = manager.request_allocation(
        workload_id="workload-1",
        requirements=ComputeRequirements(
            capabilities=frozenset(
                {ComputeCapability.AI_INFERENCE}
            )
        ),
        budget=ComputeBudget(
            max_cpu_percent=50.0,
        ),
        priority=ComputePriorityRequest(),
    )

    assert allocation is not None
    assert allocation.workload_id == "workload-1"
    assert allocation.resource.name == "cpu"


def test_manager_returns_none_when_no_resource_matches() -> None:
    manager = make_manager()

    allocation = manager.request_allocation(
        workload_id="workload-1",
        requirements=ComputeRequirements(
            capabilities=frozenset(
                {ComputeCapability.VISION}
            )
        ),
        budget=ComputeBudget(),
        priority=ComputePriorityRequest(),
    )

    assert allocation is None


def test_manager_rejects_duplicate_allocation() -> None:
    manager = make_manager()

    requirements = ComputeRequirements()

    manager.request_allocation(
        workload_id="workload-1",
        requirements=requirements,
        budget=ComputeBudget(),
        priority=ComputePriorityRequest(),
    )

    with pytest.raises(ValueError):
        manager.request_allocation(
            workload_id="workload-1",
            requirements=requirements,
            budget=ComputeBudget(),
            priority=ComputePriorityRequest(),
        )


def test_manager_allocation_lifecycle() -> None:
    manager = make_manager()

    manager.request_allocation(
        workload_id="workload-1",
        requirements=ComputeRequirements(),
        budget=ComputeBudget(),
        priority=ComputePriorityRequest(),
    )

    approved = manager.approve_allocation("workload-1")
    assert approved.state.value == "approved"

    active = manager.activate_allocation("workload-1")
    assert active.state.value == "active"

    released = manager.release_allocation("workload-1")
    assert released.state.value == "released"


def test_manager_can_reject_allocation() -> None:
    manager = make_manager()

    manager.request_allocation(
        workload_id="workload-1",
        requirements=ComputeRequirements(),
        budget=ComputeBudget(),
        priority=ComputePriorityRequest(),
    )

    rejected = manager.reject_allocation("workload-1")

    assert rejected.state.value == "rejected"


def test_manager_can_remove_allocation() -> None:
    manager = make_manager()

    manager.request_allocation(
        workload_id="workload-1",
        requirements=ComputeRequirements(),
        budget=ComputeBudget(),
        priority=ComputePriorityRequest(),
    )

    manager.remove_allocation("workload-1")

    assert len(manager.allocations) == 0


def test_manager_rejects_unknown_allocation() -> None:
    manager = make_manager()

    with pytest.raises(KeyError):
        manager.approve_allocation("unknown")
