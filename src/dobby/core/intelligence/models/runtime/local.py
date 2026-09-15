from __future__ import annotations

from typing import FrozenSet

from ..model import Model, ModelRequest, ModelResponse
from .backend import ModelExecutionBackend
from .runtime import ModelRuntime


class LocalModelRuntime(ModelRuntime):
    """Execute models locally through an internal execution backend."""

    def __init__(self, backend: ModelExecutionBackend) -> None:
        self._backend = backend

    @property
    def name(self) -> str:
        """Return the runtime name."""
        return f"local:{self._backend.name}"

    @property
    def capabilities(self) -> FrozenSet[str]:
        """Return the capabilities supported by the backend."""
        return self._backend.capabilities

    def supports(self, requirement: str) -> bool:
        """Return whether the backend supports a requirement."""
        return self._backend.supports(requirement)

    def load(self, model: Model) -> None:
        """Load a model through the execution backend."""
        self._backend.load(model)

    def unload(self, model: Model) -> None:
        """Unload a model through the execution backend."""
        self._backend.unload(model)

    def is_loaded(self, model: Model) -> bool:
        """Return whether a model is loaded."""
        return self._backend.is_loaded(model)

    def generate(
        self,
        model: Model,
        request: ModelRequest,
    ) -> ModelResponse:
        """Generate a response through the execution backend."""

        if not self.is_loaded(model):
            raise RuntimeError(
                f"Model is not loaded in runtime: {self.name}"
            )

        return self._backend.generate(model, request)
