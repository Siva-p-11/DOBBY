from dataclasses import dataclass

from dobby.config.settings import DobbySettings
from dobby.core.agent import Agent
from dobby.core.executor import AgentExecutor
from dobby.core.runtime import RuntimeEnvironment, RuntimeIdentity, RuntimeState


@dataclass(slots=True)
class DobbyApplication:
    """Main application runtime for Dobby."""

    settings: DobbySettings
    identity: RuntimeIdentity
    environment: RuntimeEnvironment
    state: RuntimeState
    executor: AgentExecutor
    running: bool = False

    @classmethod
    def create(cls, settings: DobbySettings) -> "DobbyApplication":
        """Create a Dobby application from configuration."""
        identity = RuntimeIdentity.create(
            name=settings.app.name,
        )

        environment = RuntimeEnvironment.detect()

        state = RuntimeState(
            status="created",
            environment_type=settings.app.environment,
        )

        return cls(
            settings=settings,
            identity=identity,
            environment=environment,
            state=state,
            executor=AgentExecutor(),
        )

    def start(self) -> None:
        """Start the Dobby application."""
        self.running = True
        self.state = RuntimeState(
            status="running",
            environment_type=self.state.environment_type,
        )

    def stop(self) -> None:
        """Stop the Dobby application."""
        self.running = False
        self.state = RuntimeState(
            status="stopped",
            environment_type=self.state.environment_type,
        )

    def run(self, agent: Agent, task: str) -> str:
        """Execute a task using the provided agent."""
        if not self.running:
            raise RuntimeError("Dobby application is not running.")

        return self.executor.execute(agent, task)
