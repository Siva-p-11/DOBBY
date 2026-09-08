from dataclasses import dataclass, field

from dobby.core.permissions.permission import Permission, PermissionEffect
from dobby.core.permissions.rules import PermissionRule


@dataclass(slots=True)
class Policy:
    """Collection of permission rules used by Dobby."""

    rules: list[PermissionRule] = field(default_factory=list)

    def add_rule(self, rule: PermissionRule) -> None:
        """Add a permission rule to the policy."""
        self.rules.append(rule)

    def remove_rule(self, capability: str) -> None:
        """Remove rules associated with a capability."""
        self.rules = [
            rule
            for rule in self.rules
            if not rule.matches(capability)
        ]

    def get_permission(
        self,
        capability: str,
        environment: str | None = None,
        resource: str | None = None,
        context: dict[str, object] | None = None,
    ) -> Permission | None:
        """Return the permission matching the request, if defined."""

        for rule in reversed(self.rules):
            if rule.matches(
                capability=capability,
                environment=environment,
                resource=resource,
                context=context,
            ):
                return rule.permission

        return None

    def allows(
        self,
        capability: str,
        environment: str | None = None,
        resource: str | None = None,
        context: dict[str, object] | None = None,
    ) -> bool:
        """Return whether a capability is allowed by this policy."""

        permission = self.get_permission(
            capability=capability,
            environment=environment,
            resource=resource,
            context=context,
        )

        if permission is None:
            return False

        return permission.effect is PermissionEffect.ALLOW
