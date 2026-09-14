from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComputeResourceStateSnapshot:
    utilization_percent: float = 0.0

    memory_used_mb: int = 0
    memory_available_mb: int | None = None

    temperature_celsius: float | None = None
    power_watts: float | None = None

    active_user_workload: bool = False

    def __post_init__(self) -> None:
        if not 0.0 <= self.utilization_percent <= 100.0:
            raise ValueError("utilization_percent must be between 0 and 100")

        if self.memory_used_mb < 0:
            raise ValueError("memory_used_mb cannot be negative")

        if self.memory_available_mb is not None and self.memory_available_mb < 0:
            raise ValueError("memory_available_mb cannot be negative")

        if self.temperature_celsius is not None and self.temperature_celsius < -100:
            raise ValueError("temperature_celsius is unrealistically low")

        if self.power_watts is not None and self.power_watts < 0:
            raise ValueError("power_watts cannot be negative")

    @property
    def memory_pressure_percent(self) -> float | None:
        """Return memory usage as a percentage when capacity is known."""
        if self.memory_available_mb is None:
            return None

        total_memory = self.memory_used_mb + self.memory_available_mb

        if total_memory == 0:
            return 0.0

        return (self.memory_used_mb / total_memory) * 100.0
