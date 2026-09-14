from __future__ import annotations

import pytest

from dobby.core.intelligence.models.model import ModelCapability
from dobby.core.intelligence.models.requirements import (
    ModelIntensity,
    ModelLatency,
    ModelModality,
    ModelRequirements,
)


def test_default_model_requirements() -> None:
    requirements = ModelRequirements()

    assert requirements.intensity == ModelIntensity.LOW
    assert requirements.latency == ModelLatency.NORMAL
    assert requirements.modality == ModelModality.TEXT
    assert requirements.capabilities == frozenset()
    assert requirements.context_size is None
    assert requirements.memory_required_mb is None
    assert not requirements.continuous
    assert not requirements.parallel


def test_model_requirements_store_capabilities() -> None:
    requirements = ModelRequirements(
        capabilities=frozenset(
            {
                ModelCapability.REASONING,
                ModelCapability.CODING,
            }
        )
    )

    assert requirements.requires(ModelCapability.REASONING)
    assert requirements.requires(ModelCapability.CODING)
    assert not requirements.requires(ModelCapability.VISION)


def test_model_requirements_store_workload_constraints() -> None:
    requirements = ModelRequirements(
        intensity=ModelIntensity.HIGH,
        latency=ModelLatency.REALTIME,
        modality=ModelModality.VISION,
        context_size=32768,
        memory_required_mb=4096,
        continuous=True,
        parallel=True,
    )

    assert requirements.intensity == ModelIntensity.HIGH
    assert requirements.latency == ModelLatency.REALTIME
    assert requirements.modality == ModelModality.VISION
    assert requirements.context_size == 32768
    assert requirements.memory_required_mb == 4096
    assert requirements.continuous
    assert requirements.parallel


def test_model_requirements_reject_invalid_context_size() -> None:
    with pytest.raises(
        ValueError,
        match="context_size must be greater than zero",
    ):
        ModelRequirements(context_size=0)


def test_model_requirements_reject_negative_memory() -> None:
    with pytest.raises(
        ValueError,
        match="memory_required_mb cannot be negative",
    ):
        ModelRequirements(memory_required_mb=-1)
