from dataclasses import dataclass
from typing import Any, Protocol


class CapabilityHandler(Protocol):
    """Contract for an implementation that executes a capability."""

    def execute(self, arguments: dict[str, Any]) -> Any:
        """Execute the capability with the provided arguments."""
        ...


@dataclass(frozen=True, slots=True)
class Capability:
    """Definition of an ability Dobby can request."""

    name: str
    description: str
    handler: CapabilityHandler
    version: str = "1.0"
    enabled: bool = True

    def execute(self, arguments: dict[str, Any]) -> Any:
        """Execute this capability."""
        if not self.enabled:
            raise RuntimeError(f"Capability '{self.name}' is disabled.")

        return self.handler.execute(arguments)
