from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class TaskStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    goal: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    status: TaskStatus = TaskStatus.CREATED
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.goal.strip():
            raise ValueError("goal cannot be empty")

    def start(self) -> None:
        if self.status not in {
            TaskStatus.CREATED,
            TaskStatus.RUNNING,
        }:
            raise ValueError(
                f"cannot start task in status: {self.status.value}"
            )

        self.status = TaskStatus.RUNNING

    def complete(self) -> None:
        if self.status != TaskStatus.RUNNING:
            raise ValueError(
                f"cannot complete task in status: {self.status.value}"
            )

        self.status = TaskStatus.COMPLETED

    def fail(self) -> None:
        if self.status not in {
            TaskStatus.CREATED,
            TaskStatus.RUNNING,
        }:
            raise ValueError(
                f"cannot fail task in status: {self.status.value}"
            )

        self.status = TaskStatus.FAILED

    def cancel(self) -> None:
        if self.status not in {
            TaskStatus.CREATED,
            TaskStatus.RUNNING,
        }:
            raise ValueError(
                f"cannot cancel task in status: {self.status.value}"
            )

        self.status = TaskStatus.CANCELLED

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "goal": self.goal,
            "created_at": self.created_at.isoformat(),
            "status": self.status.value,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Task:
        return cls(
            id=str(data["id"]),
            goal=str(data["goal"]),
            created_at=datetime.fromisoformat(str(data["created_at"])),
            status=TaskStatus(str(data["status"])),
            metadata={
                str(key): str(value)
                for key, value in dict(data.get("metadata", {})).items()
            },
        )
