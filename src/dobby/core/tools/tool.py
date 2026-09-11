from abc import ABC, abstractmethod
from typing import Any

from dobby.core.environment.environment import Environment


class Tool(ABC):
    """Base contract for a Dobby execution tool."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique tool name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the tool does."""
        raise NotImplementedError

    @property
    def enabled(self) -> bool:
        """Return whether the tool is enabled."""
        return True

    @abstractmethod
    def execute(
        self,
        arguments: dict[str, Any],
        environment: Environment,
    ) -> Any:
        """Execute the tool inside the supplied environment."""
        raise NotImplementedError
