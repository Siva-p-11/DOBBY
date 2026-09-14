from dobby.core.compute.resource import (
    ComputeCapability,
    ComputeResource,
    ComputeResourceState,
    ComputeResourceType,
)


def make_cpu() -> ComputeResource:
    return ComputeResource(
        name="cpu",
        resource_type=ComputeResourceType.CPU,
        architecture="x86_64",
        capabilities=frozenset(
            {
                ComputeCapability.GENERAL_COMPUTE,
                ComputeCapability.LOW_LATENCY,
            }
        ),
    )


def test_resource_supports_capability() -> None:
    resource = make_cpu()

    assert resource.supports(ComputeCapability.GENERAL_COMPUTE)
    assert not resource.supports(ComputeCapability.VISION)


def test_available_resource_is_available() -> None:
    resource = make_cpu()

    assert resource.is_available()


def test_unavailable_resource_is_not_available() -> None:
    resource = make_cpu().with_state(
        ComputeResourceState.UNAVAILABLE
    )

    assert not resource.is_available()


def test_user_reserved_resource_is_not_available() -> None:
    resource = make_cpu().with_state(
        ComputeResourceState.USER_RESERVED,
        user_reserved=True,
    )

    assert not resource.is_available()


def test_with_state_preserves_resource_properties() -> None:
    resource = make_cpu()

    updated = resource.with_state(
        ComputeResourceState.THROTTLED
    )

    assert updated.name == resource.name
    assert updated.resource_type == resource.resource_type
    assert updated.architecture == resource.architecture
    assert updated.capabilities == resource.capabilities
    assert updated.state == ComputeResourceState.THROTTLED
