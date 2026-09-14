from dataclasses import dataclass
from typing import Any

from dobby.core.environment.environment import Environment
from dobby.core.permissions.evaluator import PermissionDecision
from dobby.core.permissions.evaluator import PermissionEvaluator
from dobby.core.tools.binding import ToolCapabilityBinder
from dobby.core.tools.executor import ToolExecutor
from dobby.core.tools.resolver import ToolResolver


class CapabilityExecutionError(RuntimeError):
    """Raised when capability execution cannot proceed."""


@dataclass(frozen=True, slots=True)
class CapabilityExecutionResult:
    """Result of executing a capability through a tool."""

    capability: str
    tool: str
    environment: str
    result: Any
    permission: PermissionDecision


class CapabilityExecutionService:
    """Coordinate capability resolution, policy, environment, and tool execution."""

    def __init__(
        self,
        binder: ToolCapabilityBinder,
        tool_resolver: ToolResolver,
        tool_executor: ToolExecutor,
        permission_evaluator: PermissionEvaluator,
    ) -> None:
        self._binder = binder
        self._tool_resolver = tool_resolver
        self._tool_executor = tool_executor
        self._permission_evaluator = permission_evaluator

    def execute(
        self,
        capability_name: str,
        arguments: dict[str, Any],
        environment: Environment,
    ) -> CapabilityExecutionResult:
        """Execute a capability through its bound tool."""

        permission = self._permission_evaluator.evaluate(
            capability_name,
        )

        if not permission.allowed:
            raise CapabilityExecutionError(
                f"Capability '{capability_name}' is not allowed: "
                f"{permission.reason}"
            )

        bindings = self._binder.get_for_capability(
            capability_name,
        )

        if not bindings:
            raise CapabilityExecutionError(
                f"No tool is bound to capability "
                f"'{capability_name}'."
            )

        binding = bindings[0]

        try:
            tool = self._tool_resolver.resolve(
                binding.tool_name,
            )
        except KeyError as exc:
            raise CapabilityExecutionError(
                f"Bound tool '{binding.tool_name}' "
                f"could not be resolved."
            ) from exc

        result = self._tool_executor.execute(
            tool=tool,
            arguments=arguments,
            environment=environment,
        )

        return CapabilityExecutionResult(
            capability=capability_name,
            tool=tool.name,
            environment=environment.name,
            result=result,
            permission=permission,
        )
