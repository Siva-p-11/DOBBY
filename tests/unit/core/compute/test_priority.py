from dobby.core.compute.priority import (
    ComputePriority,
    ComputePriorityRequest,
)


def test_default_priority_is_normal() -> None:
    request = ComputePriorityRequest()

    assert request.priority == ComputePriority.NORMAL


def test_higher_priority_is_detected() -> None:
    high = ComputePriorityRequest(
        priority=ComputePriority.INTERACTIVE,
    )

    low = ComputePriorityRequest(
        priority=ComputePriority.BACKGROUND,
    )

    assert high.is_higher_than(low)
    assert not low.is_higher_than(high)


def test_user_priority_is_detected() -> None:
    request = ComputePriorityRequest(
        priority=ComputePriority.USER_RESERVED,
    )

    assert request.is_user_priority()


def test_interactive_priority_is_detected() -> None:
    request = ComputePriorityRequest(
        priority=ComputePriority.INTERACTIVE,
    )

    assert request.is_interactive()
