from __future__ import annotations

from typing import FrozenSet

from dobby.core.intelligence.models.model import (
    Model,
    ModelCapability,
    ModelRequest,
    ModelResponse,
)
from dobby.core.intelligence.models.runtime.binding import ModelBinding
from dobby.core.intelligence.models.runtime.runtime import ModelRuntime
from dobby.core.intelligence.models.runtime.validation import ModelValidator
from dobby.core.intelligence.models.specification import ModelSpecification


class FakeModel(Model):
    @property
    def name(self) -> str:
        return "test-model"

    @property
    def capabilities(self) -> FrozenSet[ModelCapability]:
        return frozenset({ModelCapability.TEXT_GENERATION})


class FakeRuntime(ModelRuntime):
    def __init__(
        self,
        name: str = "fake-runtime",
        capabilities: FrozenSet[str] | None = None,
    ) -> None:
        self._name = name
        self._capabilities = capabilities or frozenset()
        self._loaded: set[str] = set()

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> FrozenSet[str]:
        return self._capabilities

    def supports(self, requirement: str) -> bool:
        return requirement in self.capabilities

    def load(self, model: Model) -> None:
        self._loaded.add(model.name)

    def unload(self, model: Model) -> None:
        self._loaded.discard(model.name)

    def is_loaded(self, model: Model) -> bool:
        return model.name in self._loaded

    def generate(
        self,
        model: Model,
        request: ModelRequest,
    ) -> ModelResponse:
        raise NotImplementedError


def make_binding(
    *,
    name: str = "test-model",
    capabilities: FrozenSet[ModelCapability] | None = None,
    runtime_requirements: FrozenSet[str] | None = None,
) -> ModelBinding:
    model = FakeModel()

    specification = ModelSpecification(
        name=name,
        version="1.0",
        capabilities=capabilities
        or frozenset({ModelCapability.TEXT_GENERATION}),
        runtime_requirements=runtime_requirements or frozenset(),
    )

    return ModelBinding(
        model=model,
        specification=specification,
    )


def test_validator_accepts_valid_binding() -> None:
    binding = make_binding()

    result = ModelValidator().validate(binding)

    assert result.valid is True
    assert result.errors == ()


def test_validator_rejects_invalid_binding() -> None:
    binding = make_binding(name="different-model")

    result = ModelValidator().validate(binding)

    assert result.valid is False
    assert "same model" in result.errors[0]


def test_validator_accepts_supported_runtime_requirements() -> None:
    binding = make_binding(
        runtime_requirements=frozenset({"cuda", "gpu"})
    )

    runtime = FakeRuntime(
        capabilities=frozenset({"cuda", "gpu"})
    )

    result = ModelValidator().validate(
        binding,
        runtime,
    )

    assert result.valid is True
    assert result.errors == ()


def test_validator_rejects_unsupported_runtime_requirements() -> None:
    binding = make_binding(
        runtime_requirements=frozenset({"cuda", "tensor_cores"})
    )

    runtime = FakeRuntime(
        capabilities=frozenset({"cuda"})
    )

    result = ModelValidator().validate(
        binding,
        runtime,
    )

    assert result.valid is False
    assert len(result.errors) == 1
    assert "tensor_cores" in result.errors[0]


def test_validator_reports_all_unsupported_requirements() -> None:
    binding = make_binding(
        runtime_requirements=frozenset(
            {
                "cuda",
                "tensor_cores",
                "fp16",
            }
        )
    )

    runtime = FakeRuntime(
        capabilities=frozenset({"cuda"})
    )

    result = ModelValidator().validate(
        binding,
        runtime,
    )

    assert result.valid is False
    assert len(result.errors) == 1
    assert "fp16" in result.errors[0]
    assert "tensor_cores" in result.errors[0]


def test_validator_without_runtime_only_validates_model_binding() -> None:
    binding = make_binding(
        runtime_requirements=frozenset({"cuda"})
    )

    result = ModelValidator().validate(binding)

    assert result.valid is True
    assert result.errors == ()
