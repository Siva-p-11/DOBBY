from typing import Any

from dobby.core.capabilities.capability import Capability


class CapabilityExecutor:
    """Execute resolved Dobby capabilities."""

    def execute(
        self,
        capability: Capability,
        arguments: dict[str, Any],
    ) -> Any:
        """Execute a capability with the supplied arguments."""
        return capability.execute(arguments)
