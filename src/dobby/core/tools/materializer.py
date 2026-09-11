from dataclasses import dataclass
from typing import Any

from dobby.core.environment.environment import Environment
from dobby.core.tools.creator import GeneratedTool
from dobby.core.tools.tool import Tool


class ToolMaterializationError(RuntimeError):
    """Raised when a generated tool cannot be materialized."""


class MaterializedTool(Tool):
    """Executable representation of a generated Dobby tool."""

    def __init__(self, generated_tool: GeneratedTool) -> None:
        self._generated_tool = generated_tool

    @property
    def name(self) -> str:
        """Return the generated tool name."""
        return self._generated_tool.specification.name

    @property
    def description(self) -> str:
        """Return the generated tool description."""
        return self._generated_tool.specification.description

    @property
    def generated_tool(self) -> GeneratedTool:
        """Return the source generated tool definition."""
        return self._generated_tool

    def execute(
        self,
        arguments: dict[str, Any],
        environment: Environment,
    ) -> Any:
        """Execute the materialized tool."""

        raise NotImplementedError(
            f"Tool '{self.name}' has no executable implementation yet."
        )


@dataclass(frozen=True, slots=True)
class ToolMaterializer:
    """Materialize generated tool definitions into executable tools."""

    def materialize(
        self,
        generated_tool: GeneratedTool,
    ) -> MaterializedTool:
        """Create an executable tool representation."""

        self._validate_generated_tool(generated_tool)

        return MaterializedTool(
            generated_tool=generated_tool,
        )

    def _validate_generated_tool(
        self,
        generated_tool: GeneratedTool,
    ) -> None:
        """Validate that a generated tool can be materialized."""

        if not generated_tool.specification.name.strip():
            raise ToolMaterializationError(
                "Generated tool requires a non-empty name."
            )

        if not generated_tool.specification.description.strip():
            raise ToolMaterializationError(
                "Generated tool requires a non-empty description."
            )

        if not generated_tool.specification.purpose.strip():
            raise ToolMaterializationError(
                "Generated tool requires a non-empty purpose."
            )
