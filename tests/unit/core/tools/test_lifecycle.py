import pytest

from dobby.core.tools.lifecycle import (
    InvalidToolLifecycleTransition,
    ToolLifecycleManager,
    ToolLifecycleState,
)


def test_tool_lifecycle_states_exist() -> None:
    assert ToolLifecycleState.PROPOSED.value == "proposed"
    assert ToolLifecycleState.GENERATED.value == "generated"
    assert ToolLifecycleState.VALIDATED.value == "validated"
    assert ToolLifecycleState.TESTED.value == "tested"
    assert ToolLifecycleState.APPROVED.value == "approved"
    assert ToolLifecycleState.ACTIVE.value == "active"
    assert ToolLifecycleState.FAILED.value == "failed"
    assert ToolLifecycleState.DISABLED.value == "disabled"
    assert ToolLifecycleState.REMOVED.value == "removed"


def test_valid_lifecycle_transition() -> None:
    manager = ToolLifecycleManager()

    result = manager.transition(
        ToolLifecycleState.PROPOSED,
        ToolLifecycleState.GENERATED,
    )

    assert result is ToolLifecycleState.GENERATED


def test_invalid_lifecycle_transition_is_rejected() -> None:
    manager = ToolLifecycleManager()

    with pytest.raises(InvalidToolLifecycleTransition):
        manager.transition(
            ToolLifecycleState.PROPOSED,
            ToolLifecycleState.ACTIVE,
        )


def test_tool_can_progress_to_active() -> None:
    manager = ToolLifecycleManager()

    state = ToolLifecycleState.PROPOSED

    for target in [
        ToolLifecycleState.GENERATED,
        ToolLifecycleState.VALIDATED,
        ToolLifecycleState.TESTED,
        ToolLifecycleState.APPROVED,
        ToolLifecycleState.ACTIVE,
    ]:
        state = manager.transition(state, target)

    assert state is ToolLifecycleState.ACTIVE


def test_active_tool_can_be_disabled() -> None:
    manager = ToolLifecycleManager()

    assert manager.can_transition(
        ToolLifecycleState.ACTIVE,
        ToolLifecycleState.DISABLED,
    )


def test_disabled_tool_can_be_reactivated() -> None:
    manager = ToolLifecycleManager()

    assert manager.can_transition(
        ToolLifecycleState.DISABLED,
        ToolLifecycleState.ACTIVE,
    )


def test_removed_tool_cannot_transition() -> None:
    manager = ToolLifecycleManager()

    assert not manager.can_transition(
        ToolLifecycleState.REMOVED,
        ToolLifecycleState.ACTIVE,
    )

    with pytest.raises(InvalidToolLifecycleTransition):
        manager.transition(
            ToolLifecycleState.REMOVED,
            ToolLifecycleState.ACTIVE,
        )


def test_failed_tool_can_return_to_proposed() -> None:
    manager = ToolLifecycleManager()

    assert manager.can_transition(
        ToolLifecycleState.FAILED,
        ToolLifecycleState.PROPOSED,
    )


def test_failed_tool_can_be_removed() -> None:
    manager = ToolLifecycleManager()

    assert manager.can_transition(
        ToolLifecycleState.FAILED,
        ToolLifecycleState.REMOVED,
    )
