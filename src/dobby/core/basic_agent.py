from dobby.core.agent import Agent


class BasicAgent(Agent):
    """Minimal concrete agent used to validate the agent runtime."""

    @property
    def name(self) -> str:
        return "basic-agent"

    def run(self, task: str) -> str:
        return f"Task received: {task}"
