from dataclasses import dataclass
from importlib.metadata import version
import platform


@dataclass(frozen=True, slots=True)
class RuntimeIdentity:
    """Identity information about the running Dobby instance."""

    name: str
    version: str
    environment: str
    python_version: str

    @classmethod
    def create(
        cls,
        name: str,
        environment: str,
    ) -> "RuntimeIdentity":
        """Create runtime identity from application configuration."""
        return cls(
            name=name,
            version=version("dobby"),
            environment=environment,
            python_version=platform.python_version(),
        )
