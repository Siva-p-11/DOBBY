from __future__ import annotations

from abc import ABC, abstractmethod
from typing import FrozenSet

from ..model import Model, ModelRequest, ModelResponse


class ModelExecutionBackend(ABC):
    """Define the contract for an internal model execution backend."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the backend name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def capabilities(self) -> FrozenSet[str]:
        """Return the features supported by this backend."""
        raise NotImplementedError

    def supports(self, requirement: str) -> bool:
        """Return whether the backend supports a requirement."""
        return requirement in self.capabilities

    @abstractmethod
    def load(self, model: Model) -> None:
        """Load a model into the backend."""
        raise NotImplementedError

    @abstractmethod
    def unload(self, model: Model) -> None:
        """Unload a model from the backend."""
        raise NotImplementedError

    @abstractmethod
    def is_loaded(self, model: Model) -> bool:
        """Return whether a model is loaded."""
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        model: Model,
        request: ModelRequest,
    ) -> ModelResponse:
        """Generate a response using a loaded model."""
        raise NotImplementedError
