from dobby.core.compute.requirements import (
    ComputeIntensity,
    ComputeLatency,
    ComputeModality,
    ComputeRequirements,
)
from dobby.core.compute.resource import ComputeCapability


def test_default_requirements() -> None:
    requirements = ComputeRequirements()

    assert requirements.intensity == ComputeIntensity.LOW
    assert requirements.latency == ComputeLatency.NORMAL
    assert requirements.modality == ComputeModality.TEXT
    assert not requirements.continuous
    assert not requirements.parallel


def test_requirements_contains_capabilities() -> None:
    requirements = ComputeRequirements(
        capabilities=frozenset(
            {
                ComputeCapability.AI_INFERENCE,
                ComputeCapability.LOW_LATENCY,
            }
        )
    )

    assert requirements.requires(ComputeCapability.AI_INFERENCE)
    assert requirements.requires(ComputeCapability.LOW_LATENCY)
    assert not requirements.requires(ComputeCapability.VISION)


def test_requirements_accept_memory_requirement() -> None:
    requirements = ComputeRequirements(
        memory_required_mb=4096,
    )

    assert requirements.memory_required_mb == 4096


def test_requirements_accept_workload_properties() -> None:
    requirements = ComputeRequirements(
        intensity=ComputeIntensity.HIGH,
        latency=ComputeLatency.REALTIME,
        modality=ComputeModality.MULTIMODAL,
        continuous=True,
        parallel=True,
    )

    assert requirements.intensity == ComputeIntensity.HIGH
    assert requirements.latency == ComputeLatency.REALTIME
    assert requirements.modality == ComputeModality.MULTIMODAL
    assert requirements.continuous
    assert requirements.parallel
