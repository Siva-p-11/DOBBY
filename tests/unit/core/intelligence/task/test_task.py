from dobby.core.intelligence.task import Task, TaskStatus


def test_task_starts_in_created_state() -> None:
    task = Task(goal="Build Dobby")

    assert task.status == TaskStatus.CREATED
    assert task.goal == "Build Dobby"


def test_task_lifecycle() -> None:
    task = Task(goal="Build Dobby")

    task.start()
    assert task.status == TaskStatus.RUNNING

    task.complete()
    assert task.status == TaskStatus.COMPLETED


def test_task_can_fail() -> None:
    task = Task(goal="Build Dobby")

    task.start()
    task.fail()

    assert task.status == TaskStatus.FAILED


def test_task_can_cancel() -> None:
    task = Task(goal="Build Dobby")

    task.start()
    task.cancel()

    assert task.status == TaskStatus.CANCELLED


def test_task_rejects_empty_goal() -> None:
    try:
        Task(goal="   ")
    except ValueError as exc:
        assert str(exc) == "goal cannot be empty"
    else:
        raise AssertionError("expected ValueError")
