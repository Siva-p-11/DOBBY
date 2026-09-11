from enum import Enum


class ToolLifecycleState(str, Enum):
    """Lifecycle states of a Dobby tool."""

    PROPOSED = "proposed"
    GENERATED = "generated"
    VALIDATED = "validated"
    TESTED = "tested"
    APPROVED = "approved"
    ACTIVE = "active"
    FAILED = "failed"
    DISABLED = "disabled"
    REMOVED = "removed"


class InvalidToolLifecycleTransition(RuntimeError):
    """Raised when a tool lifecycle transition is invalid."""


class ToolLifecycleManager:
    """Manage lifecycle transitions for Dobby tools."""

    _ALLOWED_TRANSITIONS: dict[
        ToolLifecycleState,
        set[ToolLifecycleState],
    ] = {
        ToolLifecycleState.PROPOSED: {
            ToolLifecycleState.GENERATED,
            ToolLifecycleState.FAILED,
        },
        ToolLifecycleState.GENERATED: {
            ToolLifecycleState.VALIDATED,
            ToolLifecycleState.FAILED,
        },
        ToolLifecycleState.VALIDATED: {
            ToolLifecycleState.TESTED,
            ToolLifecycleState.FAILED,
        },
        ToolLifecycleState.TESTED: {
            ToolLifecycleState.APPROVED,
            ToolLifecycleState.FAILED,
        },
        ToolLifecycleState.APPROVED: {
            ToolLifecycleState.ACTIVE,
            ToolLifecycleState.DISABLED,
        },
        ToolLifecycleState.ACTIVE: {
            ToolLifecycleState.DISABLED,
            ToolLifecycleState.REMOVED,
        },
        ToolLifecycleState.DISABLED: {
            ToolLifecycleState.ACTIVE,
            ToolLifecycleState.REMOVED,
        },
        ToolLifecycleState.FAILED: {
            ToolLifecycleState.PROPOSED,
            ToolLifecycleState.REMOVED,
        },
        ToolLifecycleState.REMOVED: set(),
    }

    def can_transition(
        self,
        current: ToolLifecycleState,
        target: ToolLifecycleState,
    ) -> bool:
        """Return whether a lifecycle transition is allowed."""

        return target in self._ALLOWED_TRANSITIONS.get(current, set())

    def transition(
        self,
        current: ToolLifecycleState,
        target: ToolLifecycleState,
    ) -> ToolLifecycleState:
        """Transition a tool to a new lifecycle state."""

        if not self.can_transition(current, target):
            raise InvalidToolLifecycleTransition(
                f"Invalid tool lifecycle transition: "
                f"{current.value} -> {target.value}."
            )

        return target
