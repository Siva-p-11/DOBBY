from __future__ import annotations

from dataclasses import dataclass

from .binding import ModelBinding
from .runtime import ModelRuntime


@dataclass(frozen=True)
class ModelValidationResult:
    """Represent the result of model validation."""

    valid: bool
    errors: tuple[str, ...] = ()


class ModelValidator:
    """Validate a model binding before runtime execution."""

    def validate(
        self,
        binding: ModelBinding,
        runtime: ModelRuntime | None = None,
    ) -> ModelValidationResult:
        """Validate a model binding and optionally a target runtime."""

        errors: list[str] = []

        if not binding.matches():
            errors.append(
                "Model and specification do not describe the same model."
            )

        specification = binding.specification

        if not specification.name.strip():
            errors.append("Model specification name cannot be empty.")

        if not specification.version.strip():
            errors.append("Model specification version cannot be empty.")

        if runtime is not None:
            unsupported = tuple(
                requirement
                for requirement in specification.runtime_requirements
                if not runtime.supports(requirement)
            )

            if unsupported:
                errors.append(
                    "Runtime does not support required features: "
                    + ", ".join(sorted(unsupported))
                )

        return ModelValidationResult(
            valid=not errors,
            errors=tuple(errors),
        )
