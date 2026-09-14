from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet


class ModelCapability(str, Enum):
    """Capabilities that an AI model may provide."""

    TEXT_GENERATION = "text_generation"
    REASONING = "reasoning"
    CODING = "coding"
    VISION = "vision"
    AUDIO = "audio"
    EMBEDDING = "embedding"
    TOOL_USE = "tool_use"


@dataclass(frozen=True)
class ModelRequest:
    """Describe a request sent to an AI model."""

    prompt: str

    system_prompt: str | None = None

    capabilities: FrozenSet[ModelCapability] = field(
        default_factory=frozenset
    )

    temperature: float = 0.7
    max_tokens: int | None = None

    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.prompt.strip():
            raise ValueError("prompt cannot be empty")

        if self.temperature < 0.0:
            raise ValueError("temperature cannot be negative")

        if self.max_tokens is not None and self.max_tokens <= 0:
            raise ValueError("max_tokens must be greater than zero")


@dataclass(frozen=True)
class ModelResponse:
    """Represent the result returned by an AI model."""

    text: str

    model_name: str

    runtime_name: str

    input_tokens: int | None = None
    output_tokens: int | None = None

    metadata: dict[str, str] = field(default_factory=dict)


class Model(ABC):
    """Abstract interface describing a Dobby AI model."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique model name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def capabilities(self) -> FrozenSet[ModelCapability]:
        """Return the capabilities provided by the model."""
        raise NotImplementedError

    def supports(self, capability: ModelCapability) -> bool:
        """Return whether the model supports a capability."""

        return capability in self.capabilities
