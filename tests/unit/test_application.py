from dobby.config.settings import DobbySettings
from dobby.core.application import DobbyApplication
from dobby.core.executor import AgentExecutor


def test_application_creation():
    settings = DobbySettings()

    app = DobbyApplication.create(settings)

    assert app.settings is settings
    assert app.identity.name == settings.app.name
    assert app.identity.environment == settings.app.environment
    assert isinstance(app.executor, AgentExecutor)
    assert app.running is False


def test_application_lifecycle():
    app = DobbyApplication.create(DobbySettings())

    app.start()
    assert app.running is True

    app.stop()
    assert app.running is False
