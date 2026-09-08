from dataclasses import dataclass, field

from dobby.core.environment.environment import (
    Environment,
    EnvironmentState,
    EnvironmentType,
)


@dataclass(slots=True)
class IsolatedEnvironment(Environment):
    """Environment representing an isolated execution context."""

    _name: str
    _state: EnvironmentState = field(
        default=EnvironmentState.CREATED,
        init=False,
    )

    @property
    def name(self) -> str:
        """Return the isolated environment name."""
        return self._name

    @property
    def environment_type(self) -> EnvironmentType:
        """Return the environment type."""
        return EnvironmentType.ISOLATED

    @property
    def state(self) -> EnvironmentState:
        """Return the current environment state."""
        return self._state

    @property
    def isolated(self) -> bool:
        """Return whether this environment is isolated."""
        return True

    def start(self) -> None:
        """Mark the isolated environment as running."""
        self._state = EnvironmentState.RUNNING

    def stop(self) -> None:
        """Mark the isolated environment as stopped."""
        self._state = EnvironmentState.STOPPED
