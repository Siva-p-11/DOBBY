from dobby.core.intelligence.task import (
    Task,
    TaskWorkspace,
    WorkspaceEntryType,
)


def test_workspace_starts_empty() -> None:
    task = Task(goal="Test task")
    workspace = TaskWorkspace(task)

    assert workspace.entries == ()
    assert workspace.latest() is None


def test_workspace_appends_entries() -> None:
    task = Task(goal="Test task")
    workspace = TaskWorkspace(task)

    first = workspace.add_entry(
        source="model-a",
        entry_type=WorkspaceEntryType.OBSERVATION,
        content="First observation",
    )

    second = workspace.add_entry(
        source="model-b",
        entry_type=WorkspaceEntryType.OBSERVATION,
        content="Second observation",
    )

    assert len(workspace.entries) == 2
    assert workspace.entries[0].id == first.id
    assert workspace.entries[1].id == second.id


def test_workspace_preserves_failed_attempts() -> None:
    task = Task(goal="Test task")
    workspace = TaskWorkspace(task)

    workspace.add_entry(
        source="model-a",
        entry_type=WorkspaceEntryType.ATTEMPT,
        content="Failed approach",
        metadata={"result": "failed"},
    )

    workspace.add_entry(
        source="model-a",
        entry_type=WorkspaceEntryType.ATTEMPT,
        content="Second approach",
        metadata={"result": "success"},
    )

    attempts = workspace.get_entries(
        entry_type=WorkspaceEntryType.ATTEMPT
    )

    assert len(attempts) == 2
    assert attempts[0].content == "Failed approach"
    assert attempts[1].content == "Second approach"


def test_workspace_can_filter_by_source() -> None:
    task = Task(goal="Test task")
    workspace = TaskWorkspace(task)

    workspace.add_entry(
        source="model-a",
        entry_type=WorkspaceEntryType.MODEL_OUTPUT,
        content="A",
    )

    workspace.add_entry(
        source="model-b",
        entry_type=WorkspaceEntryType.MODEL_OUTPUT,
        content="B",
    )

    entries = workspace.get_entries(source="model-a")

    assert len(entries) == 1
    assert entries[0].content == "A"


def test_workspace_cannot_be_cleared() -> None:
    task = Task(goal="Test task")
    workspace = TaskWorkspace(task)

    try:
        workspace.clear()
    except RuntimeError as exc:
        assert "append-only" in str(exc)
    else:
        raise AssertionError("expected RuntimeError")


def test_workspace_round_trip() -> None:
    task = Task(goal="Test task")
    workspace = TaskWorkspace(task)

    workspace.add_entry(
        source="model-a",
        entry_type=WorkspaceEntryType.EVIDENCE,
        content={"value": 42},
    )

    restored = TaskWorkspace.from_dict(workspace.to_dict())

    assert restored.task.id == task.id
    assert restored.task.goal == task.goal
    assert len(restored.entries) == 1
    assert restored.entries[0].content == {"value": 42}
