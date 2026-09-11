from dobby.core.tools.registry import ToolRegistry
from dobby.core.tools.tool import Tool


class ToolResolver:
    """Resolve tool requests against the tool registry."""

    def __init__(self, registry: ToolRegistry) -> None:
        self._registry = registry

    def resolve(self, name: str) -> Tool:
        """Resolve a tool by name."""

        return self._registry.get(name)

    def exists(self, name: str) -> bool:
        """Return whether a tool can be resolved."""

        return self._registry.has(name)
