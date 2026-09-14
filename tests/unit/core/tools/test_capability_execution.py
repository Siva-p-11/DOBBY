import pytest

from dobby.core.capabilities import Capability
from dobby.core.environment.environment import (
    Environment,
    EnvironmentState,
    EnvironmentType,
)
from dobby.core.permissions import (
    Permission,
    PermissionEffect,
    PermissionEvaluator,
    PermissionRule,
    Policy,
)
from dobby.core.tools import (
    CapabilityExecutionError,
    CapabilityExecutionResult,
    Tool,
    ToolCapabilityBinder,
    ToolExecutor,
    ToolRegistry,
    ToolResolver,
)


class DummyEnvironment(Environment):
    """Execution environment used by the tests."""

    def __init__(self, name: str = "test") -> None:
        self._name = name
        self._state = EnvironmentState.CREATED

    @property
    def name(self) -> str:
        return self._name

    @property
    def environment_type(self) -> EnvironmentType:
        return EnvironmentType.HOST

    @property
    def state(self) -> EnvironmentState:
        return self._state

    @property
    def isolated(self) -> bool:
        return False

    def start(self) -> None:
        self._state = EnvironmentState.RUNNING

    def stop(self) -> None:
        self._state = EnvironmentState.STOPPED


class DummyTool(Tool):
    """Tool used by the tests."""

    @property
    def name(self) -> str:
        return "test.tool"

    @property
    def description(self) -> str:
        return "Test execution tool."

    def execute(
        self,
        arguments: dict,
        environment: Environment,
    ) -> dict:
        return {
            "arguments": arguments,
            "environment": environment.name,
        }


class DummyCapabilityHandler:
    """Capability handler used by the tests."""

    def execute(self, arguments: dict) -> dict:
        return arguments


def create_service(
    capability_name: str = "test.capability",
) -> tuple[
    object,
    ToolRegistry,
    ToolCapabilityBinder,
    DummyEnvironment,
]:
    """Create a fully wired capability execution service."""

    tool = DummyTool()

    capability = Capability(
        name=capability_name,
        description="Test capability.",
        handler=DummyCapabilityHandler(),
    )

    tool_registry = ToolRegistry()
    tool_registry.register(tool)

    tool_resolver = ToolResolver(tool_registry)

    binder = ToolCapabilityBinder()
    binder.bind(tool, capability)

    permission = Permission(
        capability=capability_name,
        effect=PermissionEffect.ALLOW,
    )

    policy = Policy(
        rules=[
            PermissionRule(
                permission=permission,
            ),
        ],
    )

    permission_evaluator = PermissionEvaluator(policy)

    environment = DummyEnvironment()
    environment.start()

    from dobby.core.tools import CapabilityExecutionService

    service = CapabilityExecutionService(
        binder=binder,
        tool_resolver=tool_resolver,
        tool_executor=ToolExecutor(),
        permission_evaluator=permission_evaluator,
    )

    return (
        service,
        tool_registry,
        binder,
        environment,
    )


def test_service_executes_bound_capability() -> None:
    service, _, _, environment = create_service()

    result = service.execute(
        capability_name="test.capability",
        arguments={"value": 42},
        environment=environment,
    )

    assert result.result == {
        "arguments": {"value": 42},
        "environment": "test",
    }


def test_execution_result_contains_capability() -> None:
    service, _, _, environment = create_service()

    result = service.execute(
        capability_name="test.capability",
        arguments={},
        environment=environment,
    )

    assert isinstance(result, CapabilityExecutionResult)
    assert result.capability == "test.capability"


def test_execution_result_contains_tool() -> None:
    service, _, _, environment = create_service()

    result = service.execute(
        capability_name="test.capability",
        arguments={},
        environment=environment,
    )

    assert result.tool == "test.tool"


def test_execution_result_contains_environment() -> None:
    service, _, _, environment = create_service()

    result = service.execute(
        capability_name="test.capability",
        arguments={},
        environment=environment,
    )

    assert result.environment == "test"


def test_execution_result_contains_permission_decision() -> None:
    service, _, _, environment = create_service()

    result = service.execute(
        capability_name="test.capability",
        arguments={},
        environment=environment,
    )

    assert result.permission.allowed is True


def test_denied_capability_is_not_executed() -> None:
    tool = DummyTool()

    capability = Capability(
        name="test.capability",
        description="Test capability.",
        handler=DummyCapabilityHandler(),
    )

    registry = ToolRegistry()
    registry.register(tool)

    binder = ToolCapabilityBinder()
    binder.bind(tool, capability)

    permission = Permission(
        capability="test.capability",
        effect=PermissionEffect.DENY,
    )

    policy = Policy(
        rules=[
            PermissionRule(
                permission=permission,
            ),
        ],
    )

    service = create_service_with_policy(
        binder=binder,
        registry=registry,
        policy=policy,
    )

    environment = DummyEnvironment()
    environment.start()

    with pytest.raises(CapabilityExecutionError):
        service.execute(
            capability_name="test.capability",
            arguments={},
            environment=environment,
        )


def test_unbound_capability_is_rejected() -> None:
    permission = Permission(
        capability="test.capability",
        effect=PermissionEffect.ALLOW,
    )

    policy = Policy(
        rules=[
            PermissionRule(
                permission=permission,
            ),
        ],
    )

    registry = ToolRegistry()
    binder = ToolCapabilityBinder()

    service = create_service_with_policy(
        binder=binder,
        registry=registry,
        policy=policy,
    )

    environment = DummyEnvironment()
    environment.start()

    with pytest.raises(CapabilityExecutionError):
        service.execute(
            capability_name="test.capability",
            arguments={},
            environment=environment,
        )


def test_missing_bound_tool_is_rejected() -> None:
    tool = DummyTool()

    capability = Capability(
        name="test.capability",
        description="Test capability.",
        handler=DummyCapabilityHandler(),
    )

    binder = ToolCapabilityBinder()
    binder.bind(tool, capability)

    permission = Permission(
        capability="test.capability",
        effect=PermissionEffect.ALLOW,
    )

    policy = Policy(
        rules=[
            PermissionRule(
                permission=permission,
            ),
        ],
    )

    registry = ToolRegistry()

    service = create_service_with_policy(
        binder=binder,
        registry=registry,
        policy=policy,
    )

    environment = DummyEnvironment()
    environment.start()

    with pytest.raises(CapabilityExecutionError):
        service.execute(
            capability_name="test.capability",
            arguments={},
            environment=environment,
        )


def test_stopped_environment_is_rejected() -> None:
    service, _, _, environment = create_service()

    environment.stop()

    with pytest.raises(RuntimeError):
        service.execute(
            capability_name="test.capability",
            arguments={},
            environment=environment,
        )


def create_service_with_policy(
    binder: ToolCapabilityBinder,
    registry: ToolRegistry,
    policy: Policy,
):
    """Create an execution service using the supplied policy."""

    from dobby.core.tools import CapabilityExecutionService

    return CapabilityExecutionService(
        binder=binder,
        tool_resolver=ToolResolver(registry),
        tool_executor=ToolExecutor(),
        permission_evaluator=PermissionEvaluator(policy),
    )
