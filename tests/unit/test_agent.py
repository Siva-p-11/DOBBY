import pytest

from dobby.core.agent import Agent


class TestAgent(Agent):
    @property
    def name(self) -> str:
        return "test-agent"

    def run(self, task: str) -> str:
        return f"completed: {task}"


def test_agent_contract():
    agent = TestAgent()

    assert agent.name == "test-agent"
    assert agent.run("hello") == "completed: hello"


def test_agent_requires_implementation():
    with pytest.raises(TypeError):
        Agent()
