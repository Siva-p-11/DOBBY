from dobby.core.basic_agent import BasicAgent
from dobby.core.executor import AgentExecutor


def test_agent_executor():
    executor = AgentExecutor()
    agent = BasicAgent()

    result = executor.execute(agent, "learn Python")

    assert result == "Task received: learn Python"
