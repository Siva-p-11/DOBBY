import os
from pathlib import Path

import yaml

from .settings import DobbySettings


def load_config(path: Path) -> DobbySettings:
    """Load YAML configuration and apply environment overrides."""
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    runtime = data.setdefault("runtime", {})
    paths = data.setdefault("paths", {})
    app = data.setdefault("app", {})

    if "DOBBY_RUNTIME__LOG_LEVEL" in os.environ:
        runtime["log_level"] = os.environ["DOBBY_RUNTIME__LOG_LEVEL"]

    if "DOBBY_APP__NAME" in os.environ:
        app["name"] = os.environ["DOBBY_APP__NAME"]

    if "DOBBY_APP__ENVIRONMENT" in os.environ:
        app["environment"] = os.environ["DOBBY_APP__ENVIRONMENT"]

    if "DOBBY_PATHS__MODEL_STORE" in os.environ:
        paths["model_store"] = os.environ["DOBBY_PATHS__MODEL_STORE"]

    if "DOBBY_PATHS__DATASET_STORE" in os.environ:
        paths["dataset_store"] = os.environ["DOBBY_PATHS__DATASET_STORE"]

    if "DOBBY_PATHS__CACHE_STORE" in os.environ:
        paths["cache_store"] = os.environ["DOBBY_PATHS__CACHE_STORE"]

    return DobbySettings.model_validate(data)
