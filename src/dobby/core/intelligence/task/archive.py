from __future__ import annotations

import json
from pathlib import Path

from .workspace import TaskWorkspace


class TaskArchive:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def archive(self, workspace: TaskWorkspace) -> Path:
        task_id = workspace.task.id
        path = self.root / f"{task_id}.json"

        temporary_path = self.root / f".{task_id}.tmp"

        with temporary_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                workspace.to_dict(),
                file,
                ensure_ascii=False,
                indent=2,
            )
            file.write("\n")

        temporary_path.replace(path)

        return path

    def get(self, task_id: str) -> TaskWorkspace | None:
        path = self.root / f"{task_id}.json"

        if not path.exists():
            return None

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        return TaskWorkspace.from_dict(data)

    def exists(self, task_id: str) -> bool:
        return (self.root / f"{task_id}.json").exists()

    def delete(self, task_id: str) -> None:
        path = self.root / f"{task_id}.json"

        if path.exists():
            path.unlink()

    def list_task_ids(self) -> tuple[str, ...]:
        task_ids = [
            path.stem
            for path in self.root.glob("*.json")
            if path.is_file()
        ]

        return tuple(sorted(task_ids))
