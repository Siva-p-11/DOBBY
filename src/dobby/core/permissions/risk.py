from enum import IntEnum

from dobby.core.permissions.change import PolicyChange


class PolicyRiskLevel(IntEnum):
    """Risk level assigned to a policy change."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


class PolicyRiskClassifier:
    """Classify policy changes according to their security impact."""

    def classify(self, change: PolicyChange) -> PolicyRiskLevel:
        """Return the risk level for a policy change."""

        if change.change_type.value == "delete":
            return PolicyRiskLevel.HIGH

        if change.rule is None:
            return PolicyRiskLevel.HIGH

        if change.rule.environment == "cyber_lab":
            return PolicyRiskLevel.MEDIUM

        if change.change_type.value == "add":
            return PolicyRiskLevel.LOW

        return PolicyRiskLevel.MEDIUM
