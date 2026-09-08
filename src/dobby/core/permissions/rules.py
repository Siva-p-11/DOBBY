from dataclasses import dataclass, field
from typing import Any

from dobby.core.permissions.permission import Permission


@dataclass(frozen=True, slots=True)
class PermissionRule:
    """A rule that associates a capability with a permission."""

    permission: Permission
    environment: str | None = None
    resource: str | None = None
    conditions: dict[str, Any] = field(default_factory=dict)

    def matches(
        self,
        capability: str,
        environment: str | None = None,
        resource: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """Return whether this rule applies to the request."""

        if self.permission.capability != capability:
            return False

        if (
            self.environment is not None
            and self.environment != environment
        ):
            return False

        if self.resource is not None and self.resource != resource:
            return False

        if self.conditions:
            if context is None:
                return False

            for key, expected_value in self.conditions.items():
                if context.get(key) != expected_value:
                    return False

        return True
