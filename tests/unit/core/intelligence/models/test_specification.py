from __future__ import annotations

import pytest

from dobby.core.intelligence.models.model import ModelCapability
from dobby.core.intelligence.models.specification import (
    ModelArchitecture,
    ModelQuantization,
    ModelSpecification,
)


def test_default_model_specification() -> None:
    specification = ModelSpecification(
        name="test-model",
        version="1.0.0",
    )

    assert specification.name == "test-model"
    assert specification.version == "1.0.0"
    assert specification.architecture == ModelArchitecture.UNKNOWN
    assert specification.capabilities == frozenset()
    assert specification.parameter_count is None
    assert specification.context_size is None
    assert specification.memory_required_mb is None
    assert specification.quantization == ModelQuantization.NONE
    assert specification.model_path is None
    assert specification.tokenizer_path is None
    assert specification.runtime_requirements == frozenset()
    assert specification.metadata == {}


def test_model_specification_stores_model_details() -> None:
    specification = ModelSpecification(
        name="dobby-coder",
        version="1.2.0",
        architecture=ModelArchitecture.TRANSFORMER,
        capabilities=frozenset(
            {
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CODING,
            }
        ),
        parameter_count=7_000_000_000,
        context_size=32_768,
        memory_required_mb=8_192,
        quantization=ModelQuantization.INT4,
        model_path="/models/dobby-coder",
        tokenizer_path="/models/dobby-coder/tokenizer",
        runtime_requirements=frozenset(
            {
                "cuda",
                "transformers",
            }
        ),
        metadata={"source": "local"},
    )

    assert specification.name == "dobby-coder"
    assert specification.version == "1.2.0"
    assert specification.architecture == ModelArchitecture.TRANSFORMER
    assert ModelCapability.CODING in specification.capabilities
    assert specification.parameter_count == 7_000_000_000
    assert specification.context_size == 32_768
    assert specification.memory_required_mb == 8_192
    assert specification.quantization == ModelQuantization.INT4
    assert specification.model_path == "/models/dobby-coder"
    assert specification.tokenizer_path == (
        "/models/dobby-coder/tokenizer"
    )
    assert "cuda" in specification.runtime_requirements
    assert "transformers" in specification.runtime_requirements
    assert specification.metadata["source"] == "local"


def test_model_specification_supports_capability() -> None:
    specification = ModelSpecification(
        name="vision-model",
        version="1.0.0",
        capabilities=frozenset(
            {
                ModelCapability.TEXT_GENERATION,
                ModelCapability.VISION,
            }
        ),
    )

    assert specification.supports(ModelCapability.VISION)
    assert specification.supports(ModelCapability.TEXT_GENERATION)
    assert not specification.supports(ModelCapability.CODING)


def test_model_specification_rejects_empty_name() -> None:
    with pytest.raises(
        ValueError,
        match="name cannot be empty",
    ):
        ModelSpecification(
            name="   ",
            version="1.0.0",
        )


def test_model_specification_rejects_empty_version() -> None:
    with pytest.raises(
        ValueError,
        match="version cannot be empty",
    ):
        ModelSpecification(
            name="test-model",
            version="   ",
        )


def test_model_specification_rejects_invalid_parameter_count() -> None:
    with pytest.raises(
        ValueError,
        match="parameter_count must be greater than zero",
    ):
        ModelSpecification(
            name="test-model",
            version="1.0.0",
            parameter_count=0,
        )


def test_model_specification_rejects_invalid_context_size() -> None:
    with pytest.raises(
        ValueError,
        match="context_size must be greater than zero",
    ):
        ModelSpecification(
            name="test-model",
            version="1.0.0",
            context_size=0,
        )


def test_model_specification_rejects_invalid_memory_requirement() -> None:
    with pytest.raises(
        ValueError,
        match="memory_required_mb must be greater than zero",
    ):
        ModelSpecification(
            name="test-model",
            version="1.0.0",
            memory_required_mb=0,
        )
