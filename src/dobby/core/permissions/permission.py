from dataclasses import dataclass
from enum import Enum


class PermissionEffect(str, Enum):
    """Effect produced when a permission is evaluated."""

    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True, slots=True)
class Permission:
    """A permission describing whether an operation may be performed."""

    capability: str
    effect: PermissionEffect
