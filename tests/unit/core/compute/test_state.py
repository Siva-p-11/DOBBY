import pytest

from dobby.core.compute.state import ComputeResourceStateSnapshot


def test_default_state() -> None:
    state = ComputeResourceStateSnapshot()

    assert state.utilization_percent == 0.0
    assert state.memory_used_mb == 0
    assert state.memory_available_mb is None
    assert not state.active_user_workload


def test_memory_pressure_is_calculated() -> None:
    state = ComputeResourceStateSnapshot(
        memory_used_mb=4000,
        memory_available_mb=6000,
    )

    assert state.memory_pressure_percent == pytest.approx(40.0)


def test_zero_memory_returns_zero_pressure() -> None:
    state = ComputeResourceStateSnapshot(
        memory_used_mb=0,
        memory_available_mb=0,
    )

    assert state.memory_pressure_percent == 0.0


def test_unknown_memory_capacity_returns_none() -> None:
    state = ComputeResourceStateSnapshot(
        memory_used_mb=1000,
    )

    assert state.memory_pressure_percent is None


def test_invalid_utilization_is_rejected() -> None:
    with pytest.raises(ValueError):
        ComputeResourceStateSnapshot(
            utilization_percent=101.0,
        )


def test_negative_memory_is_rejected() -> None:
    with pytest.raises(ValueError):
        ComputeResourceStateSnapshot(
            memory_used_mb=-1,
        )


def test_negative_power_is_rejected() -> None:
    with pytest.raises(ValueError):
        ComputeResourceStateSnapshot(
            power_watts=-1.0,
        )
