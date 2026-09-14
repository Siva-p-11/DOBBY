from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet

from .resource import ComputeCapability


class ComputeIntensity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ComputeLatency(str, Enum):
    REALTIME = "realtime"
    NORMAL = "normal"
    BATCH = "batch"


class ComputeModality(str, Enum):
    TEXT = "text"
    VISION = "vision"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"


@dataclass(frozen=True)
class ComputeRequirements:
    capabilities: FrozenSet[ComputeCapability] = field(
        default_factory=frozenset
    )

    intensity: ComputeIntensity = ComputeIntensity.LOW
    latency: ComputeLatency = ComputeLatency.NORMAL
    modality: ComputeModality = ComputeModality.TEXT

    memory_required_mb: int | None = None

    continuous: bool = False
    parallel: bool = False

    def requires(self, capability: ComputeCapability) -> bool:
        """Return whether this workload requires a capability."""
        return capability in self.capabilities
