import pytest

from dobby.core.tools import (
    GeneratedTool,
    ToolCreationError,
    ToolCreator,
    ToolLifecycleManager,
    ToolLifecycleState,
    ToolSpecification,
)


def create_creator() -> ToolCreator:
    """Create a ToolCreator for testing."""

    return ToolCreator(
        lifecycle_manager=ToolLifecycleManager(),
    )


def test_tool_specification_stores_definition() -> None:
    specification = ToolSpecification(
        name="web.lookup",
        description="Look up information from an approved source.",
        purpose="Retrieve information required to answer a question.",
        capabilities=("network.read",),
        environments=("host", "isolated"),
        dependencies=("requests",),
        metadata={"category": "information"},
    )

    assert specification.name == "web.lookup"
    assert specification.description.startswith("Look up")
    assert specification.purpose.startswith("Retrieve")
    assert specification.capabilities == ("network.read",)
    assert specification.environments == ("host", "isolated")
    assert specification.dependencies == ("requests",)
    assert specification.metadata["category"] == "information"


def test_tool_specification_defaults_are_empty() -> None:
    specification = ToolSpecification(
        name="test.tool",
        description="Test tool.",
        purpose="Testing.",
    )

    assert specification.capabilities == ()
    assert specification.environments == ()
    assert specification.dependencies == ()
    assert specification.metadata == {}


def test_creator_generates_tool_from_specification() -> None:
    creator = create_creator()

    specification = ToolSpecification(
        name="test.tool",
        description="Test generated tool.",
        purpose="Verify tool creation.",
    )

    generated = creator.create(specification)

    assert isinstance(generated, GeneratedTool)
    assert generated.specification is specification
    assert generated.state is ToolLifecycleState.GENERATED


def test_creator_rejects_empty_name() -> None:
    creator = create_creator()

    specification = ToolSpecification(
        name="   ",
        description="Test tool.",
        purpose="Testing.",
    )

    with pytest.raises(ToolCreationError):
        creator.create(specification)


def test_creator_rejects_empty_description() -> None:
    creator = create_creator()

    specification = ToolSpecification(
        name="test.tool",
        description="   ",
        purpose="Testing.",
    )

    with pytest.raises(ToolCreationError):
        creator.create(specification)


def test_creator_rejects_empty_purpose() -> None:
    creator = create_creator()

    specification = ToolSpecification(
        name="test.tool",
        description="Test tool.",
        purpose="   ",
    )

    with pytest.raises(ToolCreationError):
        creator.create(specification)


def test_generated_tool_starts_in_generated_state() -> None:
    creator = create_creator()

    generated = creator.create(
        ToolSpecification(
            name="test.tool",
            description="Test generated tool.",
            purpose="Testing lifecycle state.",
        )
    )

    assert generated.state is ToolLifecycleState.GENERATED
