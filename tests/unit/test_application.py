from dobby.config.settings import DobbySettings
from dobby.core.application import DobbyApplication
from dobby.core.executor import AgentExecutor


def test_application_creation():
    settings = DobbySettings()

    app = DobbyApplication.create(settings)

    assert app.settings is settings
    assert app.identity.name == settings.app.name
    assert isinstance(app.executor, AgentExecutor)
    assert app.environment.operating_system
    assert app.environment.architecture
    assert app.environment.process_id > 0
    assert app.state.status == "created"
    assert app.state.environment_type == settings.app.environment


def test_application_lifecycle():
    settings = DobbySettings()

    app = DobbyApplication.create(settings)

    assert app.running is False
    assert app.state.status == "created"

    app.start()

    assert app.running is True
    assert app.state.status == "running"

    app.stop()

    assert app.running is False
    assert app.state.status == "stopped"
