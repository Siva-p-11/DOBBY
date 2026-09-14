from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet

from .model import ModelCapability


class ModelArchitecture(str, Enum):
    """Architecture families supported by Dobby."""

    UNKNOWN = "unknown"
    TRANSFORMER = "transformer"
    CNN = "cnn"
    RNN = "rnn"
    DIFFUSION = "diffusion"
    ENCODER_DECODER = "encoder_decoder"
    HYBRID = "hybrid"


class ModelQuantization(str, Enum):
    """Quantization level used by a model."""

    NONE = "none"
    INT8 = "int8"
    INT4 = "int4"
    FP16 = "fp16"
    BF16 = "bf16"
    FP8 = "fp8"


@dataclass(frozen=True)
class ModelSpecification:
    """Describe the technical characteristics of a local model."""

    name: str

    version: str

    architecture: ModelArchitecture = ModelArchitecture.UNKNOWN

    capabilities: FrozenSet[ModelCapability] = field(
        default_factory=frozenset
    )

    parameter_count: int | None = None

    context_size: int | None = None

    memory_required_mb: int | None = None

    quantization: ModelQuantization = ModelQuantization.NONE

    model_path: str | None = None

    tokenizer_path: str | None = None

    runtime_requirements: FrozenSet[str] = field(
        default_factory=frozenset
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )

    def supports(self, capability: ModelCapability) -> bool:
        """Return whether the model supports a capability."""

        return capability in self.capabilities

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name cannot be empty")

        if not self.version.strip():
            raise ValueError("version cannot be empty")

        if self.parameter_count is not None and self.parameter_count <= 0:
            raise ValueError(
                "parameter_count must be greater than zero"
            )

        if self.context_size is not None and self.context_size <= 0:
            raise ValueError(
                "context_size must be greater than zero"
            )

        if (
            self.memory_required_mb is not None
            and self.memory_required_mb <= 0
        ):
            raise ValueError(
                "memory_required_mb must be greater than zero"
            )
