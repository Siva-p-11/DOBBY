import pytest

from dobby.core.environment.environment import EnvironmentState
from dobby.core.environment.host import HostEnvironment
from dobby.core.environment.isolated import IsolatedEnvironment
from dobby.core.environment.manager import EnvironmentManager


def test_register_environment() -> None:
    """Manager should register an environment."""

    manager = EnvironmentManager()
    host = HostEnvironment()

    manager.register(host)

    assert len(manager) == 1
    assert manager.has("host") is True
    assert manager.get("host") is host


def test_register_duplicate_environment_is_rejected() -> None:
    """Duplicate environment names should be rejected."""

    manager = EnvironmentManager()

    manager.register(HostEnvironment())

    with pytest.raises(ValueError):
        manager.register(HostEnvironment())


def test_get_unknown_environment_is_rejected() -> None:
    """Unknown environments should raise an error."""

    manager = EnvironmentManager()

    with pytest.raises(KeyError):
        manager.get("unknown")


def test_unregister_environment() -> None:
    """Manager should remove a registered environment."""

    manager = EnvironmentManager()
    host = HostEnvironment()

    manager.register(host)
    manager.unregister("host")

    assert len(manager) == 0
    assert manager.has("host") is False


def test_unregister_unknown_environment_is_rejected() -> None:
    """Removing an unknown environment should raise an error."""

    manager = EnvironmentManager()

    with pytest.raises(KeyError):
        manager.unregister("unknown")


def test_list_environments() -> None:
    """Manager should return all registered environments."""

    manager = EnvironmentManager()

    host = HostEnvironment()
    cyber_lab = IsolatedEnvironment("cyber_lab")

    manager.register(host)
    manager.register(cyber_lab)

    environments = manager.list()

    assert environments == [host, cyber_lab]


def test_start_environment() -> None:
    """Manager should start a registered environment."""

    manager = EnvironmentManager()
    host = HostEnvironment()

    manager.register(host)
    manager.start("host")

    assert host.state is EnvironmentState.RUNNING


def test_stop_environment() -> None:
    """Manager should stop a registered environment."""

    manager = EnvironmentManager()
    cyber_lab = IsolatedEnvironment("cyber_lab")

    manager.register(cyber_lab)
    manager.start("cyber_lab")
    manager.stop("cyber_lab")

    assert cyber_lab.state is EnvironmentState.STOPPED


def test_start_already_running_environment_is_safe() -> None:
    """Starting an already running environment should be harmless."""

    manager = EnvironmentManager()
    host = HostEnvironment()

    manager.register(host)

    manager.start("host")
    manager.start("host")

    assert host.state is EnvironmentState.RUNNING


def test_stop_already_stopped_environment_is_safe() -> None:
    """Stopping an already stopped environment should be harmless."""

    manager = EnvironmentManager()
    host = HostEnvironment()

    manager.register(host)

    manager.stop("host")
    manager.stop("host")

    assert host.state is EnvironmentState.STOPPED
