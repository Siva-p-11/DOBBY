import pytest

from dobby.core.capabilities import Capability
from dobby.core.tools import (
    Tool,
    ToolCapabilityBinder,
    ToolCapabilityBinding,
    ToolCapabilityBindingError,
)


class TestTool(Tool):
    """Test tool implementation."""

    @property
    def name(self) -> str:
        return "test.tool"

    @property
    def description(self) -> str:
        return "Test tool."

    def execute(self, arguments, environment):
        return arguments


class TestCapabilityHandler:
    """Test capability handler."""

    def execute(self, arguments):
        return arguments


def create_tool() -> Tool:
    """Create a test tool."""

    return TestTool()


def create_capability() -> Capability:
    """Create a test capability."""

    return Capability(
        name="test.capability",
        description="Test capability.",
        handler=TestCapabilityHandler(),
    )


def create_binder() -> ToolCapabilityBinder:
    """Create a tool-capability binder."""

    return ToolCapabilityBinder()


def test_binding_stores_tool_and_capability() -> None:
    tool = create_tool()
    capability = create_capability()

    binding = ToolCapabilityBinding(
        tool=tool,
        capability=capability,
    )

    assert binding.tool is tool
    assert binding.capability is capability


def test_binding_exposes_names() -> None:
    binding = ToolCapabilityBinding(
        tool=create_tool(),
        capability=create_capability(),
    )

    assert binding.tool_name == "test.tool"
    assert binding.capability_name == "test.capability"


def test_binder_creates_binding() -> None:
    binder = create_binder()

    binding = binder.bind(
        tool=create_tool(),
        capability=create_capability(),
    )

    assert isinstance(binding, ToolCapabilityBinding)
    assert len(binder) == 1


def test_binder_detects_existing_binding() -> None:
    binder = create_binder()

    binder.bind(
        tool=create_tool(),
        capability=create_capability(),
    )

    assert binder.has_binding(
        tool_name="test.tool",
        capability_name="test.capability",
    )


def test_binder_rejects_duplicate_binding() -> None:
    binder = create_binder()

    tool = create_tool()
    capability = create_capability()

    binder.bind(tool, capability)

    with pytest.raises(ToolCapabilityBindingError):
        binder.bind(tool, capability)


def test_get_bindings_for_tool() -> None:
    binder = create_binder()

    tool = create_tool()
    capability = create_capability()

    binder.bind(tool, capability)

    bindings = binder.get_for_tool("test.tool")

    assert len(bindings) == 1
    assert bindings[0].tool is tool


def test_get_bindings_for_capability() -> None:
    binder = create_binder()

    tool = create_tool()
    capability = create_capability()

    binder.bind(tool, capability)

    bindings = binder.get_for_capability("test.capability")

    assert len(bindings) == 1
    assert bindings[0].capability is capability


def test_binder_lists_all_bindings() -> None:
    binder = create_binder()

    binder.bind(
        create_tool(),
        create_capability(),
    )

    assert len(binder.list()) == 1


def test_unbind_removes_binding() -> None:
    binder = create_binder()

    binder.bind(
        create_tool(),
        create_capability(),
    )

    binder.unbind(
        tool_name="test.tool",
        capability_name="test.capability",
    )

    assert len(binder) == 0


def test_unbind_unknown_binding_raises() -> None:
    binder = create_binder()

    with pytest.raises(KeyError):
        binder.unbind(
            tool_name="missing.tool",
            capability_name="missing.capability",
        )


def test_binding_rejects_empty_tool_name() -> None:
    class EmptyNameTool(TestTool):
        @property
        def name(self) -> str:
            return "   "

    with pytest.raises(ToolCapabilityBindingError):
        ToolCapabilityBinding(
            tool=EmptyNameTool(),
            capability=create_capability(),
        )


def test_binding_rejects_empty_capability_name() -> None:
    class EmptyNameHandler:
        def execute(self, arguments):
            return arguments

    capability = Capability(
        name="   ",
        description="Test capability.",
        handler=EmptyNameHandler(),
    )

    with pytest.raises(ToolCapabilityBindingError):
        ToolCapabilityBinding(
            tool=create_tool(),
            capability=capability,
        )
