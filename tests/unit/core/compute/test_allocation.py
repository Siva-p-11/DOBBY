from dobby.core.compute.allocation import (
    ComputeAllocation,
    ComputeAllocationState,
)
from dobby.core.compute.budget import ComputeBudget
from dobby.core.compute.priority import ComputePriorityRequest
from dobby.core.compute.requirements import ComputeRequirements
from dobby.core.compute.resource import (
    ComputeResource,
    ComputeResourceType,
)


def make_allocation() -> ComputeAllocation:
    resource = ComputeResource(
        name="cpu",
        resource_type=ComputeResourceType.CPU,
        architecture="x86_64",
    )

    return ComputeAllocation(
        workload_id="test-workload",
        resource=resource,
        requirements=ComputeRequirements(),
        budget=ComputeBudget(),
        priority=ComputePriorityRequest(),
    )


def test_allocation_starts_requested() -> None:
    allocation = make_allocation()

    assert allocation.state == ComputeAllocationState.REQUESTED


def test_allocation_can_be_approved() -> None:
    allocation = make_allocation()

    approved = allocation.approve()

    assert approved.state == ComputeAllocationState.APPROVED
    assert allocation.state == ComputeAllocationState.REQUESTED


def test_allocation_can_be_activated() -> None:
    allocation = make_allocation()

    active = allocation.activate()

    assert active.state == ComputeAllocationState.ACTIVE


def test_allocation_can_be_released() -> None:
    allocation = make_allocation()

    released = allocation.release()

    assert released.state == ComputeAllocationState.RELEASED


def test_allocation_can_be_rejected() -> None:
    allocation = make_allocation()

    rejected = allocation.reject()

    assert rejected.state == ComputeAllocationState.REJECTED
