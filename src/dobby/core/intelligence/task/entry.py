from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class WorkspaceEntryType(str, Enum):
    OBSERVATION = "observation"
    ACTION = "action"
    TOOL_RESULT = "tool_result"
    HYPOTHESIS = "hypothesis"
    DECISION = "decision"
    ATTEMPT = "attempt"
    EVIDENCE = "evidence"
    ARTIFACT = "artifact"
    STATUS = "status"
    MODEL_OUTPUT = "model_output"


@dataclass(frozen=True)
class WorkspaceEntry:
    task_id: str
    source: str
    entry_type: WorkspaceEntryType
    content: Any
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id cannot be empty")

        if not self.source.strip():
            raise ValueError("source cannot be empty")

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "source": self.source,
            "entry_type": self.entry_type.value,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> WorkspaceEntry:
        return cls(
            id=str(data["id"]),
            task_id=str(data["task_id"]),
            source=str(data["source"]),
            entry_type=WorkspaceEntryType(str(data["entry_type"])),
            content=data.get("content"),
            created_at=datetime.fromisoformat(str(data["created_at"])),
            metadata={
                str(key): str(value)
                for key, value in dict(data.get("metadata", {})).items()
            },
        )
