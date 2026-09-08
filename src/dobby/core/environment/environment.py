from abc import ABC, abstractmethod
from enum import Enum


class EnvironmentType(str, Enum):
    """Types of environments available to Dobby."""

    HOST = "host"
    ISOLATED = "isolated"


class EnvironmentState(str, Enum):
    """Lifecycle states of an environment."""

    CREATED = "created"
    RUNNING = "running"
    STOPPED = "stopped"


class Environment(ABC):
    """Base contract for a Dobby execution environment."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the environment name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def environment_type(self) -> EnvironmentType:
        """Return the environment type."""
        raise NotImplementedError

    @property
    @abstractmethod
    def state(self) -> EnvironmentState:
        """Return the current environment state."""
        raise NotImplementedError

    @property
    @abstractmethod
    def isolated(self) -> bool:
        """Return whether the environment is isolated."""
        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        """Start the environment."""
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """Stop the environment."""
        raise NotImplementedError
