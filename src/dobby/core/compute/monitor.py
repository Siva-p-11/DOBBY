from __future__ import annotations

from abc import ABC, abstractmethod

from .resource import ComputeResource
from .state import ComputeResourceStateSnapshot


class ComputeResourceMonitor(ABC):
    """Interface for obtaining live compute resource state."""

    @abstractmethod
    def snapshot(
        self,
        resource: ComputeResource,
    ) -> ComputeResourceStateSnapshot:
        """Return the current state of a compute resource."""
        raise NotImplementedError
