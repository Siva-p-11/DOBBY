from __future__ import annotations

from .runtime import ModelRuntime


class ModelRuntimeManager:
    """Manage the runtimes available to Dobby."""

    def __init__(self) -> None:
        self._runtimes: dict[str, ModelRuntime] = {}

    @property
    def runtimes(self) -> tuple[ModelRuntime, ...]:
        """Return all registered runtimes."""

        return tuple(self._runtimes.values())

    def register(self, runtime: ModelRuntime) -> None:
        """Register a runtime."""

        if runtime.name in self._runtimes:
            raise ValueError(
                f"Runtime already registered: {runtime.name}"
            )

        self._runtimes[runtime.name] = runtime

    def unregister(self, runtime_name: str) -> None:
        """Remove a registered runtime."""

        if runtime_name not in self._runtimes:
            raise KeyError(
                f"Unknown runtime: {runtime_name}"
            )

        del self._runtimes[runtime_name]

    def get(self, runtime_name: str) -> ModelRuntime:
        """Return a registered runtime by name."""

        try:
            return self._runtimes[runtime_name]
        except KeyError as exc:
            raise KeyError(
                f"Unknown runtime: {runtime_name}"
            ) from exc
