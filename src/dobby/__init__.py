from pathlib import Path

from dobby.config.loader import load_config
from dobby.core.application import DobbyApplication


def main() -> None:
    """Start the Dobby application."""
    config_path = Path("configs/default.yaml")

    settings = load_config(config_path)
    app = DobbyApplication.create(settings)

    app.start()

    print(
        f"{app.identity.name} "
        f"v{app.identity.version} "
        f"({app.identity.environment})"
    )
