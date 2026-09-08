from dataclasses import dataclass, field

from dobby.core.environment.environment import (
    Environment,
    EnvironmentState,
    EnvironmentType,
)


@dataclass(slots=True)
class HostEnvironment(Environment):
    """Environment representing the physical host running Dobby."""

    _state: EnvironmentState = field(
        default=EnvironmentState.CREATED,
        init=False,
    )

    @property
    def name(self) -> str:
        """Return the host environment name."""
        return "host"

    @property
    def environment_type(self) -> EnvironmentType:
        """Return the environment type."""
        return EnvironmentType.HOST

    @property
    def state(self) -> EnvironmentState:
        """Return the current host state."""
        return self._state

    @property
    def isolated(self) -> bool:
        """Return whether the host is isolated."""
        return False

    def start(self) -> None:
        """Mark the host environment as running."""
        self._state = EnvironmentState.RUNNING

    def stop(self) -> None:
        """Mark the host environment as stopped."""
        self._state = EnvironmentState.STOPPED
