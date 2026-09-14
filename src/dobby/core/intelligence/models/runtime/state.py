from __future__ import annotations

from enum import Enum


class ModelRuntimeState(str, Enum):
    """Represent the lifecycle state of a model in a runtime."""

    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    UNLOADING = "unloading"

