from dobby.core.environment.environment import (
    EnvironmentState,
    EnvironmentType,
)
from dobby.core.environment.isolated import IsolatedEnvironment


def test_isolated_environment_properties() -> None:
    """Isolated environment should expose the correct properties."""

    environment = IsolatedEnvironment("cyber_lab")

    assert environment.name == "cyber_lab"
    assert environment.environment_type is EnvironmentType.ISOLATED
    assert environment.isolated is True
    assert environment.state is EnvironmentState.CREATED


def test_isolated_environment_start() -> None:
    """Starting an isolated environment should update its state."""

    environment = IsolatedEnvironment("cyber_lab")

    environment.start()

    assert environment.state is EnvironmentState.RUNNING


def test_isolated_environment_stop() -> None:
    """Stopping an isolated environment should update its state."""

    environment = IsolatedEnvironment("cyber_lab")

    environment.start()
    environment.stop()

    assert environment.state is EnvironmentState.STOPPED
