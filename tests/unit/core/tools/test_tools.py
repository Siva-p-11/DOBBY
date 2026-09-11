import pytest

from dobby.core.environment import (
    EnvironmentState,
    HostEnvironment,
)
from dobby.core.tools import (
    Tool,
    ToolExecutor,
    ToolRegistry,
    ToolResolver,
)


class ExampleTool(Tool):
    """Test tool implementation."""

    @property
    def name(self) -> str:
        return "example.tool"

    @property
    def description(self) -> str:
        return "Example tool for testing."

    def execute(
        self,
        arguments: dict[str, object],
        environment: HostEnvironment,
    ) -> str:
        return f"{environment.name}:{arguments['value']}"


class DisabledTool(ExampleTool):
    """Disabled test tool."""

    @property
    def enabled(self) -> bool:
        return False


def test_tool_requires_implementation() -> None:
    with pytest.raises(TypeError):
        Tool()  # type: ignore[abstract]


def test_registry_registers_tool() -> None:
    registry = ToolRegistry()
    tool = ExampleTool()

    registry.register(tool)

    assert registry.has("example.tool")
    assert registry.get("example.tool") is tool
    assert len(registry) == 1


def test_registry_rejects_duplicate_tool() -> None:
    registry = ToolRegistry()
    tool = ExampleTool()

    registry.register(tool)

    with pytest.raises(ValueError):
        registry.register(tool)


def test_registry_unregisters_tool() -> None:
    registry = ToolRegistry()
    registry.register(ExampleTool())

    registry.unregister("example.tool")

    assert not registry.has("example.tool")
    assert len(registry) == 0


def test_registry_rejects_unknown_tool() -> None:
    registry = ToolRegistry()

    with pytest.raises(KeyError):
        registry.get("unknown.tool")


def test_registry_lists_tools() -> None:
    registry = ToolRegistry()
    tool = ExampleTool()

    registry.register(tool)

    assert list(registry.list()) == [tool]


def test_resolver_resolves_registered_tool() -> None:
    registry = ToolRegistry()
    tool = ExampleTool()
    registry.register(tool)

    resolver = ToolResolver(registry)

    assert resolver.resolve("example.tool") is tool
    assert resolver.exists("example.tool")


def test_resolver_rejects_unknown_tool() -> None:
    registry = ToolRegistry()
    resolver = ToolResolver(registry)

    with pytest.raises(KeyError):
        resolver.resolve("unknown.tool")

    assert not resolver.exists("unknown.tool")


def test_executor_executes_tool_in_environment() -> None:
    registry = ToolRegistry()
    tool = ExampleTool()
    registry.register(tool)

    resolver = ToolResolver(registry)
    executor = ToolExecutor()

    environment = HostEnvironment()
    environment.start()

    resolved_tool = resolver.resolve("example.tool")

    result = executor.execute(
        tool=resolved_tool,
        arguments={"value": "hello"},
        environment=environment,
    )

    assert result == "host:hello"


def test_executor_rejects_disabled_tool() -> None:
    executor = ToolExecutor()
    environment = HostEnvironment()
    environment.start()

    with pytest.raises(RuntimeError):
        executor.execute(
            tool=DisabledTool(),
            arguments={"value": "hello"},
            environment=environment,
        )


def test_executor_rejects_stopped_environment() -> None:
    executor = ToolExecutor()
    environment = HostEnvironment()

    with pytest.raises(RuntimeError):
        executor.execute(
            tool=ExampleTool(),
            arguments={"value": "hello"},
            environment=environment,
        )
