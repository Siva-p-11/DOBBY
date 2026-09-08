from typing import Any

import pytest

from dobby.core.capabilities import (
    Capability,
    CapabilityExecutor,
    CapabilityResolver,
    CapabilityRegistry,
)


class MockCapabilityHandler:
    """Simple handler used to test capability execution."""

    def __init__(self) -> None:
        self.received_arguments: dict[str, Any] | None = None

    def execute(self, arguments: dict[str, Any]) -> Any:
        """Execute the mock capability."""
        self.received_arguments = arguments
        return {
            "success": True,
            "arguments": arguments,
        }


def create_capability(
    name: str = "test.capability",
) -> tuple[Capability, MockCapabilityHandler]:
    """Create a test capability and its handler."""
    handler = MockCapabilityHandler()

    capability = Capability(
        name=name,
        description="Test capability",
        handler=handler,
    )

    return capability, handler


def test_capability_executes_handler() -> None:
    capability, handler = create_capability()

    arguments = {"message": "hello"}

    result = capability.execute(arguments)

    assert result == {
        "success": True,
        "arguments": arguments,
    }

    assert handler.received_arguments == arguments


def test_disabled_capability_cannot_execute() -> None:
    handler = MockCapabilityHandler()

    capability = Capability(
        name="disabled.capability",
        description="Disabled test capability",
        handler=handler,
        enabled=False,
    )

    with pytest.raises(RuntimeError, match="disabled"):
        capability.execute({})


def test_registry_registers_capability() -> None:
    registry = CapabilityRegistry()
    capability, _ = create_capability()

    registry.register(capability)

    assert registry.has("test.capability")
    assert registry.get("test.capability") is capability
    assert len(registry) == 1


def test_registry_rejects_duplicate_capability() -> None:
    registry = CapabilityRegistry()
    capability, _ = create_capability()

    registry.register(capability)

    with pytest.raises(ValueError, match="already registered"):
        registry.register(capability)


def test_registry_unregisters_capability() -> None:
    registry = CapabilityRegistry()
    capability, _ = create_capability()

    registry.register(capability)
    registry.unregister("test.capability")

    assert not registry.has("test.capability")
    assert len(registry) == 0


def test_registry_rejects_unknown_capability() -> None:
    registry = CapabilityRegistry()

    with pytest.raises(KeyError, match="not registered"):
        registry.get("unknown.capability")


def test_resolver_resolves_registered_capability() -> None:
    registry = CapabilityRegistry()
    capability, _ = create_capability()

    registry.register(capability)

    resolver = CapabilityResolver(registry)

    assert resolver.exists("test.capability")
    assert resolver.resolve("test.capability") is capability


def test_resolver_rejects_unknown_capability() -> None:
    registry = CapabilityRegistry()
    resolver = CapabilityResolver(registry)

    assert not resolver.exists("unknown.capability")

    with pytest.raises(KeyError, match="not registered"):
        resolver.resolve("unknown.capability")


def test_executor_executes_capability() -> None:
    capability, handler = create_capability()
    executor = CapabilityExecutor()

    arguments = {"value": 42}

    result = executor.execute(capability, arguments)

    assert result == {
        "success": True,
        "arguments": arguments,
    }

    assert handler.received_arguments == arguments
