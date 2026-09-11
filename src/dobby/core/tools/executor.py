from typing import Any

from dobby.core.environment.environment import Environment
from dobby.core.tools.tool import Tool


class ToolExecutor:
    """Execute resolved Dobby tools."""

    def execute(
        self,
        tool: Tool,
        arguments: dict[str, Any],
        environment: Environment,
    ) -> Any:
        """Execute the tool inside the supplied environment."""

        if not tool.enabled:
            raise RuntimeError(
                f"Tool '{tool.name}' is disabled."
            )

        if environment.state.value != "running":
            raise RuntimeError(
                f"Environment '{environment.name}' is not running."
            )

        return tool.execute(
            arguments=arguments,
            environment=environment,
        )
