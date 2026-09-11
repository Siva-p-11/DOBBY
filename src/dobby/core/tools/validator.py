from dataclasses import dataclass

from dobby.core.tools.lifecycle import ToolLifecycleState
from dobby.core.tools.tool import Tool


@dataclass(frozen=True, slots=True)
class ToolValidationResult:
    """Result of validating a Dobby tool."""

    valid: bool
    reasons: tuple[str, ...]


class ToolValidator:
    """Validate Dobby tools before they enter the active lifecycle."""

    def validate(
        self,
        tool: Tool,
        state: ToolLifecycleState,
    ) -> ToolValidationResult:
        """Validate a tool against the current lifecycle state."""

        reasons: list[str] = []

        if not tool.name.strip():
            reasons.append("Tool name cannot be empty.")

        if not tool.description.strip():
            reasons.append("Tool description cannot be empty.")

        if not tool.enabled:
            reasons.append("Tool is disabled.")

        if state in {
            ToolLifecycleState.REMOVED,
            ToolLifecycleState.FAILED,
        }:
            reasons.append(
                f"Tool cannot be validated from lifecycle state "
                f"'{state.value}'."
            )

        return ToolValidationResult(
            valid=not reasons,
            reasons=tuple(reasons),
        )
