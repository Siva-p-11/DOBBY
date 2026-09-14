from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet

from .model import ModelCapability


class ModelIntensity(str, Enum):
    """Expected computational intensity of a model workload."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ModelLatency(str, Enum):
    """Latency requirement for a model workload."""

    REALTIME = "realtime"
    NORMAL = "normal"
    BATCH = "batch"


class ModelModality(str, Enum):
    """Primary input modality required by a model workload."""

    TEXT = "text"
    VISION = "vision"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"


@dataclass(frozen=True)
class ModelRequirements:
    """Describe the capabilities and constraints required from a model."""

    capabilities: FrozenSet[ModelCapability] = field(
        default_factory=frozenset
    )

    intensity: ModelIntensity = ModelIntensity.LOW
    latency: ModelLatency = ModelLatency.NORMAL
    modality: ModelModality = ModelModality.TEXT

    context_size: int | None = None
    memory_required_mb: int | None = None

    continuous: bool = False
    parallel: bool = False

    def requires(self, capability: ModelCapability) -> bool:
        """Return whether this workload requires a capability."""

        return capability in self.capabilities

    def __post_init__(self) -> None:
        if self.context_size is not None and self.context_size <= 0:
            raise ValueError(
                "context_size must be greater than zero"
            )

        if (
            self.memory_required_mb is not None
            and self.memory_required_mb < 0
        ):
            raise ValueError(
                "memory_required_mb cannot be negative"
            )
