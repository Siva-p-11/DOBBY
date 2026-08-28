from dobby.core.agent import Agent


class AgentExecutor:
    """Execute tasks using a Dobby agent."""

    def execute(self, agent: Agent, task: str) -> str:
        """Execute a task using the provided agent."""
        return agent.run(task)
