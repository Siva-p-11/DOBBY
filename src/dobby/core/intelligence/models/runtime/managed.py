from __future__ import annotations

from dataclasses import dataclass

from ..model import Model
from .runtime import ModelRuntime
from .state import ModelRuntimeState


@dataclass
class ManagedModel:
    """Track a model managed by a runtime."""

    model: Model
    runtime: ModelRuntime
    state: ModelRuntimeState = ModelRuntimeState.UNLOADED

    def load(self) -> None:
        """Load the model into its runtime."""

        if self.state == ModelRuntimeState.LOADED:
            return

        if self.state != ModelRuntimeState.UNLOADED:
            raise RuntimeError(
                f"Cannot load model from state: {self.state.value}"
            )

        self.state = ModelRuntimeState.LOADING

        try:
            self.runtime.load(self.model)
        except Exception:
            self.state = ModelRuntimeState.UNLOADED
            raise

        self.state = ModelRuntimeState.LOADED

    def unload(self) -> None:
        """Unload the model from its runtime."""

        if self.state == ModelRuntimeState.UNLOADED:
            return

        if self.state != ModelRuntimeState.LOADED:
            raise RuntimeError(
                f"Cannot unload model from state: {self.state.value}"
            )

        self.state = ModelRuntimeState.UNLOADING

        try:
            self.runtime.unload(self.model)
        except Exception:
            self.state = ModelRuntimeState.LOADED
            raise

        self.state = ModelRuntimeState.UNLOADED

    def is_loaded(self) -> bool:
        """Return whether the model is currently loaded."""

        return self.state == ModelRuntimeState.LOADED
