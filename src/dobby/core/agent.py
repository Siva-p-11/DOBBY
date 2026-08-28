from abc import ABC, abstractmethod


class Agent(ABC):
    """Base contract for a Dobby agent."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the agent name."""
        raise NotImplementedError

    @abstractmethod
    def run(self, task: str) -> str:
        """Execute a task and return the result."""
        raise NotImplementedError
