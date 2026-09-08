from pathlib import Path

import pytest

from dobby.core.permissions import (
    PermissionEffect,
    PolicyLoader,
)


def write_policy(tmp_path: Path, content: str) -> Path:
    """Write temporary policy data for testing."""
    policy_file = tmp_path / "rules.yaml"
    policy_file.write_text(content, encoding="utf-8")
    return policy_file


def test_loader_loads_policy() -> None:
    loader = PolicyLoader()

    policy = loader.load("config/policy/rules.yaml")

    assert len(policy.rules) == 5


def test_loader_loads_allow_rule(tmp_path: Path) -> None:
    policy_file = write_policy(
        tmp_path,
        """
rules:
  - capability: filesystem.read
    effect: allow
""",
    )

    policy = PolicyLoader().load(policy_file)

    permission = policy.get_permission("filesystem.read")

    assert permission is not None
    assert permission.effect is PermissionEffect.ALLOW


def test_loader_loads_deny_rule(tmp_path: Path) -> None:
    policy_file = write_policy(
        tmp_path,
        """
rules:
  - capability: filesystem.delete
    effect: deny
""",
    )

    policy = PolicyLoader().load(policy_file)

    permission = policy.get_permission("filesystem.delete")

    assert permission is not None
    assert permission.effect is PermissionEffect.DENY


def test_loader_loads_environment_rule(tmp_path: Path) -> None:
    policy_file = write_policy(
        tmp_path,
        """
rules:
  - capability: security.scan
    environment: cyber_lab
    effect: allow
""",
    )

    policy = PolicyLoader().load(policy_file)

    rule = policy.rules[0]

    assert rule.environment == "cyber_lab"


def test_loader_loads_resource_rule(tmp_path: Path) -> None:
    policy_file = write_policy(
        tmp_path,
        """
rules:
  - capability: filesystem.write
    resource: /home/dobby
    effect: allow
""",
    )

    policy = PolicyLoader().load(policy_file)

    rule = policy.rules[0]

    assert rule.resource == "/home/dobby"


def test_loader_loads_conditions(tmp_path: Path) -> None:
    policy_file = write_policy(
        tmp_path,
        """
rules:
  - capability: process.execute
    effect: allow
    conditions:
      approved: true
      risk_level: low
""",
    )

    policy = PolicyLoader().load(policy_file)

    rule = policy.rules[0]

    assert rule.conditions == {
        "approved": True,
        "risk_level": "low",
    }


def test_loader_rejects_missing_file(tmp_path: Path) -> None:
    loader = PolicyLoader()

    with pytest.raises(FileNotFoundError):
        loader.load(tmp_path / "missing.yaml")


def test_loader_rejects_invalid_root(tmp_path: Path) -> None:
    policy_file = write_policy(
        tmp_path,
        """
- invalid
- policy
""",
    )

    with pytest.raises(
        ValueError,
        match="must contain a YAML mapping",
    ):
        PolicyLoader().load(policy_file)


def test_loader_rejects_missing_rules(tmp_path: Path) -> None:
    policy_file = write_policy(
        tmp_path,
        """
name: invalid
""",
    )

    with pytest.raises(
        ValueError,
        match="must contain a 'rules' list",
    ):
        PolicyLoader().load(policy_file)


def test_loader_rejects_invalid_effect(tmp_path: Path) -> None:
    policy_file = write_policy(
        tmp_path,
        """
rules:
  - capability: filesystem.read
    effect: maybe
""",
    )

    with pytest.raises(
        ValueError,
        match="Invalid permission effect",
    ):
        PolicyLoader().load(policy_file)


def test_loader_rejects_missing_capability(tmp_path: Path) -> None:
    policy_file = write_policy(
        tmp_path,
        """
rules:
  - effect: allow
""",
    )

    with pytest.raises(
        ValueError,
        match="requires a non-empty 'capability'",
    ):
        PolicyLoader().load(policy_file)


def test_loader_rejects_invalid_conditions(tmp_path: Path) -> None:
    policy_file = write_policy(
        tmp_path,
        """
rules:
  - capability: filesystem.read
    effect: allow
    conditions: invalid
""",
    )

    with pytest.raises(
        ValueError,
        match="'conditions' must be a mapping",
    ):
        PolicyLoader().load(policy_file)
