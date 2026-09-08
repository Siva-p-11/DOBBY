import pytest

from dobby.core.environment.environment import (
    Environment,
    EnvironmentState,
    EnvironmentType,
)


def test_environment_types() -> None:
    """Environment types should identify host and isolated contexts."""

    assert EnvironmentType.HOST.value == "host"
    assert EnvironmentType.ISOLATED.value == "isolated"


def test_environment_states() -> None:
    """Environment states should represent the lifecycle."""

    assert EnvironmentState.CREATED.value == "created"
    assert EnvironmentState.RUNNING.value == "running"
    assert EnvironmentState.STOPPED.value == "stopped"


def test_environment_is_abstract() -> None:
    """The base environment contract cannot be instantiated directly."""

    with pytest.raises(TypeError):
        Environment()
