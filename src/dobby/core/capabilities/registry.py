from typing import Iterator

from dobby.core.capabilities.capability import Capability


class CapabilityRegistry:
    """Registry of capabilities available to Dobby."""

    def __init__(self) -> None:
        self._capabilities: dict[str, Capability] = {}

    def register(self, capability: Capability) -> None:
        """Register a capability."""
        if capability.name in self._capabilities:
            raise ValueError(
                f"Capability '{capability.name}' is already registered."
            )

        self._capabilities[capability.name] = capability

    def unregister(self, name: str) -> None:
        """Remove a capability from the registry."""
        if name not in self._capabilities:
            raise KeyError(f"Capability '{name}' is not registered.")

        del self._capabilities[name]

    def get(self, name: str) -> Capability:
        """Get a registered capability by name."""
        try:
            return self._capabilities[name]
        except KeyError:
            raise KeyError(
                f"Capability '{name}' is not registered."
            ) from None

    def has(self, name: str) -> bool:
        """Check whether a capability is registered."""
        return name in self._capabilities

    def list(self) -> Iterator[Capability]:
        """Return all registered capabilities."""
        return iter(self._capabilities.values())

    def __len__(self) -> int:
        """Return the number of registered capabilities."""
        return len(self._capabilities)
