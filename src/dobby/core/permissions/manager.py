from dataclasses import dataclass

from dobby.core.permissions.authentication.authority import (
    AuthenticationAuthority,
)
from dobby.core.permissions.change import PolicyChange, PolicyChangeType
from dobby.core.permissions.policy import Policy
from dobby.core.permissions.risk import (
    PolicyRiskClassifier,
    PolicyRiskLevel,
)


class PolicyChangeRejected(RuntimeError):
    """Raised when a policy change cannot be applied."""


@dataclass(frozen=True, slots=True)
class PolicyChangeResult:
    """Result of applying a policy change."""

    change: PolicyChange
    risk_level: PolicyRiskLevel
    applied: bool
    reason: str


class PolicyManager:
    """Manage validated and authenticated changes to Dobby's policy."""

    def __init__(
        self,
        policy: Policy,
        risk_classifier: PolicyRiskClassifier,
        authentication_authority: AuthenticationAuthority,
    ) -> None:
        self._policy = policy
        self._risk_classifier = risk_classifier
        self._authentication_authority = authentication_authority

    @property
    def policy(self) -> Policy:
        """Return the currently active policy."""
        return self._policy

    def evaluate_change(
        self,
        change: PolicyChange,
    ) -> PolicyRiskLevel:
        """Determine the security risk of a proposed change."""
        return self._risk_classifier.classify(change)

    def apply_change(
        self,
        change: PolicyChange,
    ) -> PolicyChangeResult:
        """Validate, authenticate, and apply a policy change."""

        self._validate_change(change)

        risk_level = self.evaluate_change(change)

        if risk_level >= PolicyRiskLevel.MEDIUM:
            authenticated = self._authentication_authority.authenticate(
                risk_level
            )

            if not authenticated:
                raise PolicyChangeRejected(
                    "Authentication failed. Policy change was rejected."
                )

        self._apply(change)

        return PolicyChangeResult(
            change=change,
            risk_level=risk_level,
            applied=True,
            reason="Policy change applied successfully.",
        )

    def _validate_change(self, change: PolicyChange) -> None:
        """Validate the structure of a requested policy change."""

        if not change.capability:
            raise ValueError(
                "Policy change requires a non-empty capability."
            )

        if change.change_type in {
            PolicyChangeType.ADD,
            PolicyChangeType.MODIFY,
        }:
            if change.rule is None:
                raise ValueError(
                    "Add and modify changes require a permission rule."
                )

        if change.change_type is PolicyChangeType.DELETE:
            if change.rule is not None:
                raise ValueError(
                    "Delete changes must not contain a replacement rule."
                )

    def _apply(self, change: PolicyChange) -> None:
        """Apply a validated policy change."""

        if change.change_type is PolicyChangeType.ADD:
            if self._policy.get_permission(change.capability) is not None:
                raise PolicyChangeRejected(
                    f"Capability '{change.capability}' already has a rule."
                )

            self._policy.add_rule(change.rule)  # type: ignore[arg-type]
            return

        if change.change_type is PolicyChangeType.MODIFY:
            self._policy.remove_rule(change.capability)
            self._policy.add_rule(change.rule)  # type: ignore[arg-type]
            return

        if change.change_type is PolicyChangeType.DELETE:
            self._policy.remove_rule(change.capability)
            return

        raise PolicyChangeRejected(
            f"Unsupported policy change type: {change.change_type}."
        )
