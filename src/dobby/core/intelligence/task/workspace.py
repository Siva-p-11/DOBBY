from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .entry import WorkspaceEntry, WorkspaceEntryType
from .task import Task


@dataclass
class TaskWorkspace:
    task: Task
    _entries: list[WorkspaceEntry] = field(default_factory=list)

    def add_entry(
        self,
        source: str,
        entry_type: WorkspaceEntryType,
        content: Any,
        metadata: dict[str, str] | None = None,
    ) -> WorkspaceEntry:
        entry = WorkspaceEntry(
            task_id=self.task.id,
            source=source,
            entry_type=entry_type,
            content=content,
            metadata=dict(metadata or {}),
        )

        self._entries.append(entry)
        return entry

    @property
    def entries(self) -> tuple[WorkspaceEntry, ...]:
        return tuple(self._entries)

    def get_entries(
        self,
        *,
        entry_type: WorkspaceEntryType | None = None,
        source: str | None = None,
    ) -> tuple[WorkspaceEntry, ...]:
        results = self._entries

        if entry_type is not None:
            results = [
                entry
                for entry in results
                if entry.entry_type == entry_type
            ]

        if source is not None:
            results = [
                entry
                for entry in results
                if entry.source == source
            ]

        return tuple(results)

    def latest(self) -> WorkspaceEntry | None:
        if not self._entries:
            return None

        return self._entries[-1]

    def clear(self) -> None:
        raise RuntimeError(
            "TaskWorkspace is append-only and cannot be cleared"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "task": self.task.to_dict(),
            "entries": [
                entry.to_dict()
                for entry in self._entries
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> TaskWorkspace:
        task = Task.from_dict(dict(data["task"]))

        entries = [
            WorkspaceEntry.from_dict(dict(entry))
            for entry in list(data.get("entries", []))
        ]

        workspace = cls(task=task)
        workspace._entries.extend(entries)

        return workspace
