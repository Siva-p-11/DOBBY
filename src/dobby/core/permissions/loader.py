from pathlib import Path
from typing import Any

import yaml

from dobby.core.permissions.permission import Permission, PermissionEffect
from dobby.core.permissions.policy import Policy
from dobby.core.permissions.rules import PermissionRule


class PolicyLoader:
    """Load Dobby policies from a YAML configuration file."""

    def load(self, path: str | Path) -> Policy:
        """Load a policy from a YAML file."""
        policy_path = Path(path)

        if not policy_path.exists():
            raise FileNotFoundError(
                f"Policy file '{policy_path}' does not exist."
            )

        with policy_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if not isinstance(data, dict):
            raise ValueError("Policy file must contain a YAML mapping.")

        rules_data = data.get("rules")

        if not isinstance(rules_data, list):
            raise ValueError("Policy file must contain a 'rules' list.")

        policy = Policy()

        for rule_data in rules_data:
            rule = self._parse_rule(rule_data)
            policy.add_rule(rule)

        return policy

    def _parse_rule(self, data: Any) -> PermissionRule:
        """Convert one YAML rule into a permission rule."""
        if not isinstance(data, dict):
            raise ValueError("Each policy rule must be a YAML mapping.")

        capability = data.get("capability")
        effect = data.get("effect")

        if not isinstance(capability, str) or not capability:
            raise ValueError(
                "Each policy rule requires a non-empty 'capability'."
            )

        if effect not in {
            PermissionEffect.ALLOW.value,
            PermissionEffect.DENY.value,
        }:
            raise ValueError(
                f"Invalid permission effect '{effect}'."
            )

        environment = data.get("environment")
        resource = data.get("resource")
        conditions = data.get("conditions", {})

        if environment is not None and not isinstance(environment, str):
            raise ValueError("'environment' must be a string.")

        if resource is not None and not isinstance(resource, str):
            raise ValueError("'resource' must be a string.")

        if not isinstance(conditions, dict):
            raise ValueError("'conditions' must be a mapping.")

        permission = Permission(
            capability=capability,
            effect=PermissionEffect(effect),
        )

        return PermissionRule(
            permission=permission,
            environment=environment,
            resource=resource,
            conditions=conditions,
        )
