from dobby.core.environment.environment import (
    Environment,
    EnvironmentState,
)


class EnvironmentManager:
    """Manage the environments available to Dobby."""

    def __init__(self) -> None:
        self._environments: dict[str, Environment] = {}

    def register(self, environment: Environment) -> None:
        """Register an environment."""

        if environment.name in self._environments:
            raise ValueError(
                f"Environment '{environment.name}' is already registered."
            )

        self._environments[environment.name] = environment

    def unregister(self, name: str) -> None:
        """Remove an environment from the manager."""

        if name not in self._environments:
            raise KeyError(
                f"Environment '{name}' is not registered."
            )

        del self._environments[name]

    def get(self, name: str) -> Environment:
        """Return a registered environment."""

        try:
            return self._environments[name]
        except KeyError:
            raise KeyError(
                f"Environment '{name}' is not registered."
            ) from None

    def has(self, name: str) -> bool:
        """Return whether an environment is registered."""

        return name in self._environments

    def list(self) -> list[Environment]:
        """Return all registered environments."""

        return list(self._environments.values())

    def start(self, name: str) -> None:
        """Start a registered environment."""

        environment = self.get(name)

        if environment.state is EnvironmentState.RUNNING:
            return

        environment.start()

    def stop(self, name: str) -> None:
        """Stop a registered environment."""

        environment = self.get(name)

        if environment.state is EnvironmentState.STOPPED:
            return

        environment.stop()

    def __len__(self) -> int:
        """Return the number of registered environments."""

        return len(self._environments)
