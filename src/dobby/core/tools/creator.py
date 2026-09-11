from dataclasses import dataclass

from dobby.core.tools.lifecycle import (
    ToolLifecycleManager,
    ToolLifecycleState,
)
from dobby.core.tools.specification import ToolSpecification


@dataclass(frozen=True, slots=True)
class GeneratedTool:
    """Representation of a tool generated from a specification."""

    specification: ToolSpecification
    state: ToolLifecycleState


class ToolCreationError(RuntimeError):
    """Raised when a tool cannot be created."""


class ToolCreator:
    """Create tool representations from tool specifications."""

    def __init__(
        self,
        lifecycle_manager: ToolLifecycleManager,
    ) -> None:
        self._lifecycle_manager = lifecycle_manager

    def create(
        self,
        specification: ToolSpecification,
    ) -> GeneratedTool:
        """Create a generated tool from a specification."""

        self._validate_specification(specification)

        state = self._lifecycle_manager.transition(
            ToolLifecycleState.PROPOSED,
            ToolLifecycleState.GENERATED,
        )

        return GeneratedTool(
            specification=specification,
            state=state,
        )

    def _validate_specification(
        self,
        specification: ToolSpecification,
    ) -> None:
        """Validate the basic structure of a tool specification."""

        if not specification.name.strip():
            raise ToolCreationError(
                "Tool specification requires a non-empty name."
            )

        if not specification.description.strip():
            raise ToolCreationError(
                "Tool specification requires a non-empty description."
            )

        if not specification.purpose.strip():
            raise ToolCreationError(
                "Tool specification requires a non-empty purpose."
            )
