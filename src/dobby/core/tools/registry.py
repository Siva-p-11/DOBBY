from typing import Iterator

from dobby.core.tools.tool import Tool


class ToolRegistry:
    """Registry of tools available to Dobby."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool."""

        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered."
            )

        self._tools[tool.name] = tool

    def unregister(self, name: str) -> None:
        """Remove a tool from the registry."""

        if name not in self._tools:
            raise KeyError(
                f"Tool '{name}' is not registered."
            )

        del self._tools[name]

    def get(self, name: str) -> Tool:
        """Return a registered tool."""

        try:
            return self._tools[name]
        except KeyError:
            raise KeyError(
                f"Tool '{name}' is not registered."
            ) from None

    def has(self, name: str) -> bool:
        """Return whether a tool is registered."""

        return name in self._tools

    def list(self) -> Iterator[Tool]:
        """Return all registered tools."""

        return iter(self._tools.values())

    def __len__(self) -> int:
        """Return the number of registered tools."""

        return len(self._tools)
