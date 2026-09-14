from __future__ import annotations

from dataclasses import dataclass

from ..model import Model
from ..specification import ModelSpecification


@dataclass(frozen=True)
class ModelBinding:
    """Bind a model identity to its specification."""

    model: Model
    specification: ModelSpecification

    def matches(self) -> bool:
        """Return whether the model and specification describe the same model."""

        return (
            self.model.name == self.specification.name
            and all(
                self.model.supports(capability)
                for capability in self.specification.capabilities
            )
        )
