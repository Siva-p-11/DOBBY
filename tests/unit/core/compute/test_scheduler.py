from dobby.core.compute.requirements import (
    ComputeIntensity,
    ComputeLatency,
    ComputeRequirements,
)
from dobby.core.compute.resource import (
    ComputeCapability,
    ComputeResource,
    ComputeResourceType,
)
from dobby.core.compute.scheduler import ComputeScheduler
from dobby.core.compute.state import ComputeResourceStateSnapshot


def make_cpu() -> ComputeResource:
    return ComputeResource(
        name="cpu",
        resource_type=ComputeResourceType.CPU,
        architecture="x86_64",
        capabilities=frozenset(
            {
                ComputeCapability.GENERAL_COMPUTE,
                ComputeCapability.AI_INFERENCE,
                ComputeCapability.LOW_LATENCY,
            }
        ),
    )


def make_gpu() -> ComputeResource:
    return ComputeResource(
        name="gpu",
        resource_type=ComputeResourceType.GPU,
        architecture="cuda",
        capabilities=frozenset(
            {
                ComputeCapability.AI_INFERENCE,
                ComputeCapability.VISION,
                ComputeCapability.PARALLEL_COMPUTE,
            }
        ),
    )


def make_npu() -> ComputeResource:
    return ComputeResource(
        name="npu",
        resource_type=ComputeResourceType.NPU,
        architecture="xdna",
        capabilities=frozenset(
            {
                ComputeCapability.AI_INFERENCE,
                ComputeCapability.LOW_LATENCY,
            }
        ),
    )


def test_scheduler_selects_matching_resource() -> None:
    scheduler = ComputeScheduler()

    gpu = make_gpu()

    requirements = ComputeRequirements(
        capabilities=frozenset(
            {ComputeCapability.VISION}
        )
    )

    states = {
        "gpu": ComputeResourceStateSnapshot(),
    }

    decision = scheduler.select(
        requirements,
        [gpu],
        states,
    )

    assert decision is not None
    assert decision.resource.name == "gpu"


def test_scheduler_rejects_missing_capability() -> None:
    scheduler = ComputeScheduler()

    cpu = make_cpu()

    requirements = ComputeRequirements(
        capabilities=frozenset(
            {ComputeCapability.VISION}
        )
    )

    states = {
        "cpu": ComputeResourceStateSnapshot(),
    }

    decision = scheduler.select(
        requirements,
        [cpu],
        states,
    )

    assert decision is None


def test_scheduler_rejects_insufficient_memory() -> None:
    scheduler = ComputeScheduler()

    gpu = make_gpu()

    requirements = ComputeRequirements(
        memory_required_mb=8000,
    )

    states = {
        "gpu": ComputeResourceStateSnapshot(
            memory_available_mb=4000,
        ),
    }

    decision = scheduler.select(
        requirements,
        [gpu],
        states,
    )

    assert decision is None


def test_scheduler_allows_unknown_memory_capacity() -> None:
    scheduler = ComputeScheduler()

    cpu = make_cpu()

    requirements = ComputeRequirements(
        memory_required_mb=8000,
    )

    states = {
        "cpu": ComputeResourceStateSnapshot(
            memory_available_mb=None,
        ),
    }

    decision = scheduler.select(
        requirements,
        [cpu],
        states,
    )

    assert decision is not None


def test_scheduler_prefers_less_utilized_resource() -> None:
    scheduler = ComputeScheduler()

    cpu_a = make_cpu()
    cpu_b = ComputeResource(
        name="cpu-b",
        resource_type=ComputeResourceType.CPU,
        architecture="x86_64",
        capabilities=cpu_a.capabilities,
    )

    states = {
        "cpu": ComputeResourceStateSnapshot(
            utilization_percent=80.0,
        ),
        "cpu-b": ComputeResourceStateSnapshot(
            utilization_percent=10.0,
        ),
    }

    decision = scheduler.select(
        ComputeRequirements(),
        [cpu_a, cpu_b],
        states,
    )

    assert decision is not None
    assert decision.resource.name == "cpu-b"


def test_scheduler_penalizes_active_user_workload() -> None:
    scheduler = ComputeScheduler()

    cpu = make_cpu()
    gpu = make_gpu()

    states = {
        "cpu": ComputeResourceStateSnapshot(
            active_user_workload=True,
        ),
        "gpu": ComputeResourceStateSnapshot(),
    }

    requirements = ComputeRequirements(
        capabilities=frozenset(
            {ComputeCapability.AI_INFERENCE}
        )
    )

    decision = scheduler.select(
        requirements,
        [cpu, gpu],
        states,
    )

    assert decision is not None
    assert decision.resource.name == "gpu"


def test_scheduler_prefers_gpu_for_high_intensity_work() -> None:
    scheduler = ComputeScheduler()

    cpu = make_cpu()
    gpu = make_gpu()

    states = {
        "cpu": ComputeResourceStateSnapshot(),
        "gpu": ComputeResourceStateSnapshot(),
    }

    requirements = ComputeRequirements(
        intensity=ComputeIntensity.HIGH,
        capabilities=frozenset(
            {ComputeCapability.AI_INFERENCE}
        ),
    )

    decision = scheduler.select(
        requirements,
        [cpu, gpu],
        states,
    )

    assert decision is not None
    assert decision.resource.name == "gpu"


def test_scheduler_prefers_npu_for_continuous_work() -> None:
    scheduler = ComputeScheduler()

    cpu = make_cpu()
    npu = make_npu()

    states = {
        "cpu": ComputeResourceStateSnapshot(),
        "npu": ComputeResourceStateSnapshot(),
    }

    requirements = ComputeRequirements(
        continuous=True,
        capabilities=frozenset(
            {ComputeCapability.AI_INFERENCE}
        ),
    )

    decision = scheduler.select(
        requirements,
        [cpu, npu],
        states,
    )

    assert decision is not None
    assert decision.resource.name == "npu"


def test_scheduler_prefers_low_latency_resource() -> None:
    scheduler = ComputeScheduler()

    cpu = make_cpu()
    gpu = make_gpu()

    states = {
        "cpu": ComputeResourceStateSnapshot(),
        "gpu": ComputeResourceStateSnapshot(),
    }

    requirements = ComputeRequirements(
        latency=ComputeLatency.REALTIME,
        capabilities=frozenset(
            {ComputeCapability.AI_INFERENCE}
        ),
    )

    decision = scheduler.select(
        requirements,
        [cpu, gpu],
        states,
    )

    assert decision is not None
    assert decision.resource.name == "cpu"
