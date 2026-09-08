from dataclasses import dataclass

import pytest

from dobby.core.permissions.change import (
    PolicyChange,
    PolicyChangeType,
)
from dobby.core.permissions.manager import (
    PolicyChangeRejected,
    PolicyManager,
)
from dobby.core.permissions.permission import (
    Permission,
    PermissionEffect,
)
from dobby.core.permissions.policy import Policy
from dobby.core.permissions.risk import (
    PolicyRiskClassifier,
    PolicyRiskLevel,
)
from dobby.core.permissions.rules import PermissionRule


@dataclass
class FakeAuthenticationAuthority:
    """Authentication authority used for manager tests."""

    result: bool
    calls: list[PolicyRiskLevel]

    def authenticate(self, risk_level: PolicyRiskLevel) -> bool:
        """Return the configured authentication result."""
        self.calls.append(risk_level)
        return self.result


def make_rule(
    capability: str,
    effect: PermissionEffect,
    environment: str | None = None,
) -> PermissionRule:
    """Create a permission rule for testing."""

    return PermissionRule(
        permission=Permission(
            capability=capability,
            effect=effect,
        ),
        environment=environment,
    )


def make_manager(
    authentication_result: bool = True,
) -> tuple[
    PolicyManager,
    Policy,
    FakeAuthenticationAuthority,
]:
    """Create a policy manager with a fake authentication authority."""

    policy = Policy()

    authority = FakeAuthenticationAuthority(
        result=authentication_result,
        calls=[],
    )

    manager = PolicyManager(
        policy=policy,
        risk_classifier=PolicyRiskClassifier(),
        authentication_authority=authority,
    )

    return manager, policy, authority


def test_low_risk_change_is_applied_without_authentication() -> None:
    manager, policy, authority = make_manager()

    change = PolicyChange(
        change_type=PolicyChangeType.ADD,
        capability="filesystem.read",
        rule=make_rule(
            "filesystem.read",
            PermissionEffect.ALLOW,
        ),
    )

    result = manager.apply_change(change)

    assert result.applied is True
    assert result.risk_level is PolicyRiskLevel.LOW
    assert authority.calls == []
    assert policy.allows("filesystem.read") is True


def test_medium_risk_change_requires_authentication() -> None:
    manager, policy, authority = make_manager(
        authentication_result=True,
    )

    change = PolicyChange(
        change_type=PolicyChangeType.ADD,
        capability="security.scan",
        rule=make_rule(
            "security.scan",
            PermissionEffect.ALLOW,
            environment="cyber_lab",
        ),
    )

    result = manager.apply_change(change)

    assert result.applied is True
    assert result.risk_level is PolicyRiskLevel.MEDIUM
    assert authority.calls == [PolicyRiskLevel.MEDIUM]
    assert policy.allows(
        "security.scan",
        environment="cyber_lab",
    ) is True


def test_medium_risk_change_is_rejected_when_authentication_fails() -> None:
    manager, policy, authority = make_manager(
        authentication_result=False,
    )

    change = PolicyChange(
        change_type=PolicyChangeType.ADD,
        capability="security.scan",
        rule=make_rule(
            "security.scan",
            PermissionEffect.ALLOW,
            environment="cyber_lab",
        ),
    )

    with pytest.raises(PolicyChangeRejected):
        manager.apply_change(change)

    assert authority.calls == [PolicyRiskLevel.MEDIUM]
    assert policy.get_permission(
        "security.scan",
        environment="cyber_lab",
    ) is None


def test_delete_change_requires_high_risk_authentication() -> None:
    manager, policy, authority = make_manager(
        authentication_result=True,
    )

    policy.add_rule(
        make_rule(
            "filesystem.delete",
            PermissionEffect.DENY,
        )
    )

    change = PolicyChange(
        change_type=PolicyChangeType.DELETE,
        capability="filesystem.delete",
    )

    result = manager.apply_change(change)

    assert result.applied is True
    assert result.risk_level is PolicyRiskLevel.HIGH
    assert authority.calls == [PolicyRiskLevel.HIGH]
    assert policy.get_permission("filesystem.delete") is None


def test_high_risk_change_is_rejected_when_authentication_fails() -> None:
    manager, policy, authority = make_manager(
        authentication_result=False,
    )

    policy.add_rule(
        make_rule(
            "filesystem.delete",
            PermissionEffect.DENY,
        )
    )

    change = PolicyChange(
        change_type=PolicyChangeType.DELETE,
        capability="filesystem.delete",
    )

    with pytest.raises(PolicyChangeRejected):
        manager.apply_change(change)

    assert authority.calls == [PolicyRiskLevel.HIGH]
    assert policy.get_permission("filesystem.delete") is not None


def test_modify_change_replaces_existing_rule() -> None:
    manager, policy, authority = make_manager(
        authentication_result=True,
    )

    policy.add_rule(
        make_rule(
            "filesystem.write",
            PermissionEffect.DENY,
        )
    )

    change = PolicyChange(
        change_type=PolicyChangeType.MODIFY,
        capability="filesystem.write",
        rule=make_rule(
            "filesystem.write",
            PermissionEffect.ALLOW,
        ),
    )

    result = manager.apply_change(change)

    assert result.applied is True
    assert result.risk_level is PolicyRiskLevel.MEDIUM
    assert authority.calls == [PolicyRiskLevel.MEDIUM]
    assert policy.allows("filesystem.write") is True


def test_modify_change_is_rejected_without_authentication() -> None:
    manager, policy, authority = make_manager(
        authentication_result=False,
    )

    policy.add_rule(
        make_rule(
            "filesystem.write",
            PermissionEffect.ALLOW,
        )
    )

    change = PolicyChange(
        change_type=PolicyChangeType.MODIFY,
        capability="filesystem.write",
        rule=make_rule(
            "filesystem.write",
            PermissionEffect.DENY,
        ),
    )

    with pytest.raises(PolicyChangeRejected):
        manager.apply_change(change)

    assert authority.calls == [PolicyRiskLevel.MEDIUM]
    assert policy.allows("filesystem.write") is True


def test_add_existing_capability_is_rejected() -> None:
    manager, policy, authority = make_manager()

    policy.add_rule(
        make_rule(
            "filesystem.read",
            PermissionEffect.ALLOW,
        )
    )

    change = PolicyChange(
        change_type=PolicyChangeType.ADD,
        capability="filesystem.read",
        rule=make_rule(
            "filesystem.read",
            PermissionEffect.DENY,
        ),
    )

    with pytest.raises(PolicyChangeRejected):
        manager.apply_change(change)

    assert authority.calls == []
    assert policy.allows("filesystem.read") is True


def test_add_change_requires_rule() -> None:
    manager, policy, authority = make_manager()

    change = PolicyChange(
        change_type=PolicyChangeType.ADD,
        capability="filesystem.read",
    )

    with pytest.raises(ValueError):
        manager.apply_change(change)

    assert authority.calls == []
    assert policy.get_permission("filesystem.read") is None


def test_modify_change_requires_rule() -> None:
    manager, policy, authority = make_manager()

    change = PolicyChange(
        change_type=PolicyChangeType.MODIFY,
        capability="filesystem.read",
    )

    with pytest.raises(ValueError):
        manager.apply_change(change)

    assert authority.calls == []
    assert policy.get_permission("filesystem.read") is None


def test_delete_change_must_not_contain_rule() -> None:
    manager, policy, authority = make_manager()

    change = PolicyChange(
        change_type=PolicyChangeType.DELETE,
        capability="filesystem.read",
        rule=make_rule(
            "filesystem.read",
            PermissionEffect.DENY,
        ),
    )

    with pytest.raises(ValueError):
        manager.apply_change(change)

    assert authority.calls == []
    assert policy.get_permission("filesystem.read") is None


def test_empty_capability_is_rejected() -> None:
    manager, policy, authority = make_manager()

    change = PolicyChange(
        change_type=PolicyChangeType.ADD,
        capability="",
        rule=make_rule(
            "",
            PermissionEffect.ALLOW,
        ),
    )

    with pytest.raises(ValueError):
        manager.apply_change(change)

    assert authority.calls == []
    assert len(policy.rules) == 0
