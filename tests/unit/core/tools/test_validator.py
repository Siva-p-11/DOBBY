from dobby.core.tools import (
    ToolLifecycleState,
    ToolValidator,
)
from dobby.core.tools.tool import Tool


class ValidTool(Tool):
    """Valid test tool."""

    @property
    def name(self) -> str:
        return "test.valid"

    @property
    def description(self) -> str:
        return "A valid test tool."

    def execute(
        self,
        arguments: dict[str, object],
        environment: object,
    ) -> str:
        return "success"


class EmptyNameTool(ValidTool):
    """Tool with an invalid empty name."""

    @property
    def name(self) -> str:
        return "   "


class EmptyDescriptionTool(ValidTool):
    """Tool with an invalid empty description."""

    @property
    def description(self) -> str:
        return "   "


class DisabledTool(ValidTool):
    """Disabled tool."""

    @property
    def enabled(self) -> bool:
        return False


def test_valid_tool_passes_validation() -> None:
    validator = ToolValidator()

    result = validator.validate(
        tool=ValidTool(),
        state=ToolLifecycleState.GENERATED,
    )

    assert result.valid
    assert result.reasons == ()


def test_empty_name_fails_validation() -> None:
    validator = ToolValidator()

    result = validator.validate(
        tool=EmptyNameTool(),
        state=ToolLifecycleState.GENERATED,
    )

    assert not result.valid
    assert "Tool name cannot be empty." in result.reasons


def test_empty_description_fails_validation() -> None:
    validator = ToolValidator()

    result = validator.validate(
        tool=EmptyDescriptionTool(),
        state=ToolLifecycleState.GENERATED,
    )

    assert not result.valid
    assert "Tool description cannot be empty." in result.reasons


def test_disabled_tool_fails_validation() -> None:
    validator = ToolValidator()

    result = validator.validate(
        tool=DisabledTool(),
        state=ToolLifecycleState.GENERATED,
    )

    assert not result.valid
    assert "Tool is disabled." in result.reasons


def test_removed_tool_cannot_be_validated() -> None:
    validator = ToolValidator()

    result = validator.validate(
        tool=ValidTool(),
        state=ToolLifecycleState.REMOVED,
    )

    assert not result.valid
    assert any(
        "removed" in reason
        for reason in result.reasons
    )


def test_failed_tool_cannot_be_validated() -> None:
    validator = ToolValidator()

    result = validator.validate(
        tool=ValidTool(),
        state=ToolLifecycleState.FAILED,
    )

    assert not result.valid
    assert any(
        "failed" in reason
        for reason in result.reasons
    )


def test_validation_reports_multiple_failures() -> None:
    validator = ToolValidator()

    result = validator.validate(
        tool=EmptyNameTool(),
        state=ToolLifecycleState.REMOVED,
    )

    assert not result.valid
    assert len(result.reasons) == 2
