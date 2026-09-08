from dobby.core.environment.environment import (
    EnvironmentState,
    EnvironmentType,
)
from dobby.core.environment.host import HostEnvironment


def test_host_environment_properties() -> None:
    """Host environment should expose the correct properties."""

    host = HostEnvironment()

    assert host.name == "host"
    assert host.environment_type is EnvironmentType.HOST
    assert host.isolated is False
    assert host.state is EnvironmentState.CREATED


def test_host_environment_start() -> None:
    """Starting the host environment should update its state."""

    host = HostEnvironment()

    host.start()

    assert host.state is EnvironmentState.RUNNING


def test_host_environment_stop() -> None:
    """Stopping the host environment should update its state."""

    host = HostEnvironment()

    host.start()
    host.stop()

    assert host.state is EnvironmentState.STOPPED
