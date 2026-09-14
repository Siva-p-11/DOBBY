from __future__ import annotations

from abc import ABC, abstractmethod

from ..model import Model, ModelRequest, ModelResponse


class ModelRuntime(ABC):
    """Abstract runtime responsible for executing local models."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the runtime name."""
        raise NotImplementedError

    @abstractmethod
    def load(self, model: Model) -> None:
        """Load a model into the runtime."""
        raise NotImplementedError

    @abstractmethod
    def unload(self, model: Model) -> None:
        """Unload a model from the runtime."""
        raise NotImplementedError

    @abstractmethod
    def is_loaded(self, model: Model) -> bool:
        """Return whether a model is currently loaded."""
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        model: Model,
        request: ModelRequest,
    ) -> ModelResponse:
        """Execute inference using a loaded model."""
        raise NotImplementedError
