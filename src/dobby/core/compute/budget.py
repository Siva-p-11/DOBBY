from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComputeBudget:
    """Define the maximum resources Dobby may use for a workload."""

    max_cpu_percent: float | None = None
    max_memory_mb: int | None = None
    max_gpu_memory_mb: int | None = None
    max_power_watts: float | None = None

    def __post_init__(self) -> None:
        if self.max_cpu_percent is not None:
            if not 0.0 <= self.max_cpu_percent <= 100.0:
                raise ValueError(
                    "max_cpu_percent must be between 0 and 100"
                )

        if self.max_memory_mb is not None:
            if self.max_memory_mb < 0:
                raise ValueError(
                    "max_memory_mb cannot be negative"
                )

        if self.max_gpu_memory_mb is not None:
            if self.max_gpu_memory_mb < 0:
                raise ValueError(
                    "max_gpu_memory_mb cannot be negative"
                )

        if self.max_power_watts is not None:
            if self.max_power_watts < 0:
                raise ValueError(
                    "max_power_watts cannot be negative"
                )

    def allows_cpu(self, requested_percent: float) -> bool:
        """Return whether the requested CPU usage fits the budget."""

        if requested_percent < 0.0:
            return False

        if self.max_cpu_percent is None:
            return True

        return requested_percent <= self.max_cpu_percent

    def allows_memory(self, requested_mb: int) -> bool:
        """Return whether the requested memory fits the budget."""

        if requested_mb < 0:
            return False

        if self.max_memory_mb is None:
            return True

        return requested_mb <= self.max_memory_mb

    def allows_gpu_memory(self, requested_mb: int) -> bool:
        """Return whether requested GPU memory fits the budget."""

        if requested_mb < 0:
            return False

        if self.max_gpu_memory_mb is None:
            return True

        return requested_mb <= self.max_gpu_memory_mb

    def allows_power(self, requested_watts: float) -> bool:
        """Return whether requested power fits the budget."""

        if requested_watts < 0.0:
            return False

        if self.max_power_watts is None:
            return True

        return requested_watts <= self.max_power_watts
