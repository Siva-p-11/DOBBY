from dobby.core.intelligence.task import (
    WorkspaceEntry,
    WorkspaceEntryType,
)


def test_entry_creation() -> None:
    entry = WorkspaceEntry(
        task_id="task-1",
        source="controller",
        entry_type=WorkspaceEntryType.OBSERVATION,
        content="The file exists.",
    )

    assert entry.task_id == "task-1"
    assert entry.source == "controller"
    assert entry.entry_type == WorkspaceEntryType.OBSERVATION
    assert entry.content == "The file exists."


def test_entry_preserves_metadata() -> None:
    entry = WorkspaceEntry(
        task_id="task-1",
        source="model-a",
        entry_type=WorkspaceEntryType.MODEL_OUTPUT,
        content={"answer": "test"},
        metadata={"model": "model-a"},
    )

    assert entry.metadata["model"] == "model-a"


def test_entry_is_immutable() -> None:
    entry = WorkspaceEntry(
        task_id="task-1",
        source="model-a",
        entry_type=WorkspaceEntryType.ATTEMPT,
        content="attempt",
    )

    try:
        entry.content = "changed"
    except AttributeError:
        pass
    else:
        raise AssertionError("entry should be immutable")


def test_entry_rejects_empty_source() -> None:
    try:
        WorkspaceEntry(
            task_id="task-1",
            source=" ",
            entry_type=WorkspaceEntryType.OBSERVATION,
            content="test",
        )
    except ValueError as exc:
        assert str(exc) == "source cannot be empty"
    else:
        raise AssertionError("expected ValueError")
