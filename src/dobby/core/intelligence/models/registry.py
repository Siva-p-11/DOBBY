from __future__ import annotations

from .model import Model, ModelCapability


class ModelRegistry:
    """Registry of models available to Dobby."""

    def __init__(self) -> None:
        self._models: dict[str, Model] = {}

    @property
    def models(self) -> tuple[Model, ...]:
        """Return all registered models."""

        return tuple(self._models.values())

    def register(self, model: Model) -> None:
        """Register a model."""

        if model.name in self._models:
            raise ValueError(
                f"Model already registered: {model.name}"
            )

        self._models[model.name] = model

    def unregister(self, model_name: str) -> None:
        """Remove a registered model."""

        if model_name not in self._models:
            raise KeyError(
                f"Unknown model: {model_name}"
            )

        del self._models[model_name]

    def get(self, model_name: str) -> Model:
        """Return a model by name."""

        try:
            return self._models[model_name]
        except KeyError as exc:
            raise KeyError(
                f"Unknown model: {model_name}"
            ) from exc

    def find_by_capability(
        self,
        capability: ModelCapability,
    ) -> tuple[Model, ...]:
        """Return models supporting a capability."""

        return tuple(
            model
            for model in self._models.values()
            if model.supports(capability)
        )
