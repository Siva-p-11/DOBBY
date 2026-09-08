from dataclasses import dataclass

from dobby.core.permissions.policy import Policy


@dataclass(frozen=True, slots=True)
class PermissionDecision:
    """Result of evaluating a capability against a policy."""

    capability: str
    allowed: bool
    reason: str


class PermissionEvaluator:
    """Evaluate capability requests against a policy."""

    def __init__(self, policy: Policy) -> None:
        self._policy = policy

    def evaluate(self, capability: str) -> PermissionDecision:
        """Evaluate whether a capability is allowed."""
        if self._policy.allows(capability):
            return PermissionDecision(
                capability=capability,
                allowed=True,
                reason="Capability is explicitly allowed.",
            )

        permission = self._policy.get_permission(capability)

        if permission is None:
            return PermissionDecision(
                capability=capability,
                allowed=False,
                reason="No permission rule exists for this capability.",
            )

        return PermissionDecision(
            capability=capability,
            allowed=False,
            reason="Capability is explicitly denied.",
        )
