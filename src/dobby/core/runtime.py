from dataclasses import dataclass
from importlib.metadata import version
import os
import platform


@dataclass(frozen=True, slots=True)
class RuntimeIdentity:
    """Identity information about the running Dobby instance."""

    name: str
    version: str
    python_version: str

    @classmethod
    def create(cls, name: str) -> "RuntimeIdentity":
        """Create runtime identity."""
        return cls(
            name=name,
            version=version("dobby"),
            python_version=platform.python_version(),
        )


@dataclass(frozen=True, slots=True)
class RuntimeEnvironment:
    """Information about the environment Dobby is running in."""

    operating_system: str
    architecture: str
    hostname: str
    working_directory: str
    process_id: int
    executable: str

    @classmethod
    def detect(cls) -> "RuntimeEnvironment":
        """Detect the current runtime environment."""
        return cls(
            operating_system=platform.system(),
            architecture=platform.machine(),
            hostname=platform.node(),
            working_directory=os.getcwd(),
            process_id=os.getpid(),
            executable=os.path.abspath(os.sys.executable),
        )


@dataclass(frozen=True, slots=True)
class RuntimeState:
    """Current state of the Dobby runtime."""

    status: str
    environment_type: str
