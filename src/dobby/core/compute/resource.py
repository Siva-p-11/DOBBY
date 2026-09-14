from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet


class ComputeResourceType(str, Enum):
    CPU = "cpu"
    GPU = "gpu"
    NPU = "npu"


class ComputeResourceState(str, Enum):
    AVAILABLE = "available"
    ALLOCATED = "allocated"
    USER_RESERVED = "user_reserved"
    CONSTRAINED = "constrained"
    THROTTLED = "throttled"
    UNAVAILABLE = "unavailable"


class ComputeCapability(str, Enum):
    GENERAL_COMPUTE = "general_compute"
    AI_INFERENCE = "ai_inference"
    ML_TRAINING = "ml_training"
    VISION = "vision"
    AUDIO = "audio"
    EMBEDDING = "embedding"
    LOW_LATENCY = "low_latency"
    PARALLEL_COMPUTE = "parallel_compute"


@dataclass(frozen=True)
class ComputeResource:
    name: str
    resource_type: ComputeResourceType
    architecture: str
    capabilities: FrozenSet[ComputeCapability] = field(
        default_factory=frozenset
    )

    total_memory_mb: int | None = None
    usable_memory_mb: int | None = None

    state: ComputeResourceState = ComputeResourceState.AVAILABLE

    user_reserved: bool = False

    def supports(self, capability: ComputeCapability) -> bool:
        """Return whether this resource supports a capability."""
        return capability in self.capabilities

    def is_available(self) -> bool:
        """Return whether the resource can currently accept work."""
        return self.state not in {
            ComputeResourceState.UNAVAILABLE,
            ComputeResourceState.USER_RESERVED,
        }

    def available_memory_mb(self) -> int | None:
        """Return currently usable memory available to Dobby."""
        return self.usable_memory_mb

    def with_state(
        self,
        state: ComputeResourceState,
        *,
        user_reserved: bool | None = None,
    ) -> ComputeResource:
        """Return a new resource representation with updated state."""
        return ComputeResource(
            name=self.name,
            resource_type=self.resource_type,
            architecture=self.architecture,
            capabilities=self.capabilities,
            total_memory_mb=self.total_memory_mb,
            usable_memory_mb=self.usable_memory_mb,
            state=state,
            user_reserved=(
                self.user_reserved
                if user_reserved is None
                else user_reserved
            ),
        )
