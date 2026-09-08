import pytest

from dobby.core.permissions import (
    Permission,
    PermissionDecision,
    PermissionEffect,
    PermissionEvaluator,
    PermissionRule,
    Policy,
)


def create_policy(
    capability: str = "test.capability",
    effect: PermissionEffect = PermissionEffect.ALLOW,
) -> Policy:
    """Create a policy containing one permission rule."""
    permission = Permission(
        capability=capability,
        effect=effect,
    )

    rule = PermissionRule(
        permission=permission,
    )

    policy = Policy()
    policy.add_rule(rule)

    return policy


def test_permission_defines_allow_effect() -> None:
    permission = Permission(
        capability="filesystem.read",
        effect=PermissionEffect.ALLOW,
    )

    assert permission.capability == "filesystem.read"
    assert permission.effect is PermissionEffect.ALLOW


def test_permission_rule_matches_capability() -> None:
    permission = Permission(
        capability="filesystem.read",
        effect=PermissionEffect.ALLOW,
    )

    rule = PermissionRule(permission=permission)

    assert rule.matches("filesystem.read")
    assert not rule.matches("filesystem.write")


def test_policy_allows_explicitly_allowed_capability() -> None:
    policy = create_policy()

    assert policy.allows("test.capability")


def test_policy_denies_explicitly_denied_capability() -> None:
    policy = create_policy(
        effect=PermissionEffect.DENY,
    )

    assert not policy.allows("test.capability")


def test_policy_denies_capability_without_rule() -> None:
    policy = Policy()

    assert not policy.allows("unknown.capability")
    assert policy.get_permission("unknown.capability") is None


def test_policy_can_remove_rule() -> None:
    policy = create_policy()

    assert policy.allows("test.capability")

    policy.remove_rule("test.capability")

    assert not policy.allows("test.capability")


def test_policy_latest_rule_takes_precedence() -> None:
    policy = create_policy(
        effect=PermissionEffect.ALLOW,
    )

    denied_permission = Permission(
        capability="test.capability",
        effect=PermissionEffect.DENY,
    )

    policy.add_rule(
        PermissionRule(
            permission=denied_permission,
        )
    )

    assert not policy.allows("test.capability")


def test_evaluator_allows_explicit_permission() -> None:
    policy = create_policy()

    evaluator = PermissionEvaluator(policy)

    decision = evaluator.evaluate("test.capability")

    assert isinstance(decision, PermissionDecision)
    assert decision.capability == "test.capability"
    assert decision.allowed
    assert decision.reason == "Capability is explicitly allowed."


def test_evaluator_denies_explicit_permission() -> None:
    policy = create_policy(
        effect=PermissionEffect.DENY,
    )

    evaluator = PermissionEvaluator(policy)

    decision = evaluator.evaluate("test.capability")

    assert not decision.allowed
    assert decision.reason == "Capability is explicitly denied."


def test_evaluator_denies_unknown_capability() -> None:
    policy = Policy()

    evaluator = PermissionEvaluator(policy)

    decision = evaluator.evaluate("unknown.capability")

    assert not decision.allowed
    assert decision.reason == (
        "No permission rule exists for this capability."
    )


def test_rule_matches_environment() -> None:
    permission = Permission(
        capability="filesystem.read",
        effect=PermissionEffect.ALLOW,
    )

    rule = PermissionRule(
        permission=permission,
        environment="host",
    )

    assert rule.matches(
        capability="filesystem.read",
        environment="host",
    )

    assert not rule.matches(
        capability="filesystem.read",
        environment="cyber_lab",
    )


def test_rule_matches_resource() -> None:
    permission = Permission(
        capability="filesystem.write",
        effect=PermissionEffect.ALLOW,
    )

    rule = PermissionRule(
        permission=permission,
        resource="/home/jingle/projects/dobby",
    )

    assert rule.matches(
        capability="filesystem.write",
        resource="/home/jingle/projects/dobby",
    )

    assert not rule.matches(
        capability="filesystem.write",
        resource="/etc",
    )


def test_rule_matches_conditions() -> None:
    permission = Permission(
        capability="process.execute",
        effect=PermissionEffect.ALLOW,
    )

    rule = PermissionRule(
        permission=permission,
        conditions={
            "approved": True,
            "risk_level": "low",
        },
    )

    assert rule.matches(
        capability="process.execute",
        context={
            "approved": True,
            "risk_level": "low",
        },
    )

    assert not rule.matches(
        capability="process.execute",
        context={
            "approved": False,
            "risk_level": "low",
        },
    )
