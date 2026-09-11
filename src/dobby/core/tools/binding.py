from dataclasses import dataclass

from dobby.core.capabilities.capability import Capability
from dobby.core.tools.tool import Tool


class ToolCapabilityBindingError(RuntimeError):
    """Raised when a tool-capability binding is invalid."""


@dataclass(frozen=True, slots=True)
class ToolCapabilityBinding:
    """Bind a tool to a capability it implements."""

    tool: Tool
    capability: Capability

    def __post_init__(self) -> None:
        """Validate the binding."""

        if not self.tool.name.strip():
            raise ToolCapabilityBindingError(
                "Bound tool requires a non-empty name."
            )

        if not self.capability.name.strip():
            raise ToolCapabilityBindingError(
                "Bound capability requires a non-empty name."
            )

    @property
    def tool_name(self) -> str:
        """Return the bound tool name."""

        return self.tool.name

    @property
    def capability_name(self) -> str:
        """Return the bound capability name."""

        return self.capability.name


class ToolCapabilityBinder:
    """Create and manage tool-capability bindings."""

    def __init__(self) -> None:
        self._bindings: list[ToolCapabilityBinding] = []

    def bind(
        self,
        tool: Tool,
        capability: Capability,
    ) -> ToolCapabilityBinding:
        """Bind a tool to a capability."""

        binding = ToolCapabilityBinding(
            tool=tool,
            capability=capability,
        )

        if self.has_binding(
            tool_name=tool.name,
            capability_name=capability.name,
        ):
            raise ToolCapabilityBindingError(
                f"Tool '{tool.name}' is already bound to "
                f"capability '{capability.name}'."
            )

        self._bindings.append(binding)

        return binding

    def unbind(
        self,
        tool_name: str,
        capability_name: str,
    ) -> None:
        """Remove a tool-capability binding."""

        for index, binding in enumerate(self._bindings):
            if (
                binding.tool_name == tool_name
                and binding.capability_name == capability_name
            ):
                del self._bindings[index]
                return

        raise KeyError(
            f"No binding exists between tool '{tool_name}' "
            f"and capability '{capability_name}'."
        )

    def has_binding(
        self,
        tool_name: str,
        capability_name: str,
    ) -> bool:
        """Return whether a binding exists."""

        return any(
            binding.tool_name == tool_name
            and binding.capability_name == capability_name
            for binding in self._bindings
        )

    def get_for_tool(
        self,
        tool_name: str,
    ) -> tuple[ToolCapabilityBinding, ...]:
        """Return all capability bindings for a tool."""

        return tuple(
            binding
            for binding in self._bindings
            if binding.tool_name == tool_name
        )

    def get_for_capability(
        self,
        capability_name: str,
    ) -> tuple[ToolCapabilityBinding, ...]:
        """Return all tool bindings for a capability."""

        return tuple(
            binding
            for binding in self._bindings
            if binding.capability_name == capability_name
        )

    def list(self) -> tuple[ToolCapabilityBinding, ...]:
        """Return all bindings."""

        return tuple(self._bindings)

    def __len__(self) -> int:
        """Return the number of bindings."""

        return len(self._bindings)

