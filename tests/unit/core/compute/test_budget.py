import pytest

from dobby.core.compute.budget import ComputeBudget


def test_unlimited_budget_allows_usage() -> None:
    budget = ComputeBudget()

    assert budget.allows_cpu(100.0)
    assert budget.allows_memory(100000)
    assert budget.allows_gpu_memory(100000)
    assert budget.allows_power(500.0)


def test_cpu_budget_limits_usage() -> None:
    budget = ComputeBudget(
        max_cpu_percent=50.0,
    )

    assert budget.allows_cpu(50.0)
    assert not budget.allows_cpu(50.1)


def test_memory_budget_limits_usage() -> None:
    budget = ComputeBudget(
        max_memory_mb=4096,
    )

    assert budget.allows_memory(4096)
    assert not budget.allows_memory(4097)


def test_gpu_memory_budget_limits_usage() -> None:
    budget = ComputeBudget(
        max_gpu_memory_mb=4096,
    )

    assert budget.allows_gpu_memory(4096)
    assert not budget.allows_gpu_memory(4097)


def test_power_budget_limits_usage() -> None:
    budget = ComputeBudget(
        max_power_watts=50.0,
    )

    assert budget.allows_power(50.0)
    assert not budget.allows_power(50.1)


def test_negative_cpu_request_is_rejected() -> None:
    budget = ComputeBudget()

    assert not budget.allows_cpu(-1.0)


def test_invalid_cpu_budget_is_rejected() -> None:
    with pytest.raises(ValueError):
        ComputeBudget(max_cpu_percent=101.0)


def test_negative_memory_budget_is_rejected() -> None:
    with pytest.raises(ValueError):
        ComputeBudget(max_memory_mb=-1)
