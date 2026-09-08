from dobby.core.capabilities.capability import Capability
from dobby.core.capabilities.registry import CapabilityRegistry


class CapabilityResolver:
    """Resolve capability requests against the capability registry."""

    def __init__(self, registry: CapabilityRegistry) -> None:
        self._registry = registry

    def resolve(self, name: str) -> Capability:
        """Resolve a capability by name."""
        return self._registry.get(name)

    def exists(self, name: str) -> bool:
        """Check whether a capability can be resolved."""
        return self._registry.has(name)
