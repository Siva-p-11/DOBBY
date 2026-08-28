from dobby.core.basic_agent import BasicAgent


def test_basic_agent():
    agent = BasicAgent()

    assert agent.name == "basic-agent"
    assert agent.run("learn Python") == "Task received: learn Python"
