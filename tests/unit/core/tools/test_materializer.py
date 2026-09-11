import pytest

from dobby.core.tools import (
    GeneratedTool,
    MaterializedTool,
    ToolCreator,
    ToolLifecycleManager,
    ToolMaterializationError,
    ToolMaterializer,
    ToolSpecification,
    ToolLifecycleState,
)


def create_generated_tool() -> GeneratedTool:
    """Create a valid generated tool for testing."""

    creator = ToolCreator(
        lifecycle_manager=ToolLifecycleManager(),
    )

    specification = ToolSpecification(
        name="test.tool",
        description="Test materialized tool.",
        purpose="Verify tool materialization.",
    )

    return creator.create(specification)


def create_materializer() -> ToolMaterializer:
    """Create a tool materializer for testing."""

    return ToolMaterializer()


def test_materializer_creates_materialized_tool() -> None:
    generated = create_generated_tool()
    materializer = create_materializer()

    materialized = materializer.materialize(generated)

    assert isinstance(materialized, MaterializedTool)


def test_materialized_tool_preserves_name() -> None:
    generated = create_generated_tool()
    materialized = create_materializer().materialize(generated)

    assert materialized.name == "test.tool"


def test_materialized_tool_preserves_description() -> None:
    generated = create_generated_tool()
    materialized = create_materializer().materialize(generated)

    assert materialized.description == "Test materialized tool."


def test_materialized_tool_preserves_generated_definition() -> None:
    generated = create_generated_tool()
    materialized = create_materializer().materialize(generated)

    assert materialized.generated_tool is generated


def test_materialized_tool_starts_enabled() -> None:
    generated = create_generated_tool()
    materialized = create_materializer().materialize(generated)

    assert materialized.enabled is True


def test_materialized_tool_execute_has_no_implementation_yet() -> None:
    generated = create_generated_tool()
    materialized = create_materializer().materialize(generated)

    with pytest.raises(NotImplementedError):
        materialized.execute(
            arguments={},
            environment=None,  # type: ignore[arg-type]
        )


def test_materializer_rejects_empty_name() -> None:
    creator = ToolCreator(
        lifecycle_manager=ToolLifecycleManager(),
    )

    generated = GeneratedTool(
        specification=ToolSpecification(
            name="   ",
            description="Test tool.",
            purpose="Testing.",
        ),
        state=ToolLifecycleState.GENERATED,
    )

    materializer = create_materializer()

    with pytest.raises(ToolMaterializationError):
        materializer.materialize(generated)


def test_materializer_rejects_empty_description() -> None:
    generated = GeneratedTool(
        specification=ToolSpecification(
            name="test.tool",
            description="   ",
            purpose="Testing.",
        ),
        state=ToolLifecycleState.GENERATED,
    )

    materializer = create_materializer()

    with pytest.raises(ToolMaterializationError):
        materializer.materialize(generated)


def test_materializer_rejects_empty_purpose() -> None:
    generated = GeneratedTool(
        specification=ToolSpecification(
            name="test.tool",
            description="Test tool.",
            purpose="   ",
        ),
        state=ToolLifecycleState.GENERATED,
    )

    materializer = create_materializer()

    with pytest.raises(ToolMaterializationError):
        materializer.materialize(generated)
