from dataclasses import dataclass
from enum import Enum

from dobby.core.permissions.rules import PermissionRule


class PolicyChangeType(str, Enum):
    """Type of change requested against the policy."""

    ADD = "add"
    MODIFY = "modify"
    DELETE = "delete"


@dataclass(frozen=True, slots=True)
class PolicyChange:
    """A requested change to the Dobby permission policy."""

    change_type: PolicyChangeType
    capability: str
    rule: PermissionRule | None = None
