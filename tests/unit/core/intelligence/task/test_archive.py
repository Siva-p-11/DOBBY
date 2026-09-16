from pathlib import Path

from dobby.core.intelligence.task import (
    Task,
    TaskArchive,
    TaskWorkspace,
    WorkspaceEntryType,
)


def test_archive_persists_workspace(tmp_path: Path) -> None:
    task = Task(goal="Archive test")
    workspace = TaskWorkspace(task)

    workspace.add_entry(
        source="model-a",
        entry_type=WorkspaceEntryType.OBSERVATION,
        content="Important observation",
    )

    archive = TaskArchive(tmp_path)
    path = archive.archive(workspace)

    assert path.exists()
    assert archive.exists(task.id)


def test_archive_can_restore_workspace(tmp_path: Path) -> None:
    task = Task(goal="Restore test")
    workspace = TaskWorkspace(task)

    workspace.add_entry(
        source="model-a",
        entry_type=WorkspaceEntryType.MODEL_OUTPUT,
        content="Model contribution",
    )

    archive = TaskArchive(tmp_path)
    archive.archive(workspace)

    restored = archive.get(task.id)

    assert restored is not None
    assert restored.task.id == task.id
    assert restored.task.goal == "Restore test"
    assert len(restored.entries) == 1
    assert restored.entries[0].content == "Model contribution"


def test_archive_returns_none_for_unknown_task(
    tmp_path: Path,
) -> None:
    archive = TaskArchive(tmp_path)

    assert archive.get("unknown-task") is None


def test_archive_lists_tasks(tmp_path: Path) -> None:
    archive = TaskArchive(tmp_path)

    task_a = Task(goal="Task A")
    task_b = Task(goal="Task B")

    archive.archive(TaskWorkspace(task_a))
    archive.archive(TaskWorkspace(task_b))

    task_ids = archive.list_task_ids()

    assert task_a.id in task_ids
    assert task_b.id in task_ids


def test_archive_delete(tmp_path: Path) -> None:
    archive = TaskArchive(tmp_path)

    task = Task(goal="Delete test")
    archive.archive(TaskWorkspace(task))

    assert archive.exists(task.id)

    archive.delete(task.id)

    assert not archive.exists(task.id)
