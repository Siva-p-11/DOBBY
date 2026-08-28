import os
import platform

from dobby.core.runtime import RuntimeEnvironment, RuntimeIdentity, RuntimeState

def test_runtime_identity():
    identity = RuntimeIdentity.create(name="dobby")

    assert identity.name == "dobby"
    assert identity.version == "0.1.0"
    assert identity.python_version == platform.python_version()


def test_runtime_environment():
    environment = RuntimeEnvironment.detect()

    assert environment.operating_system == platform.system()
    assert environment.architecture == platform.machine()
    assert environment.hostname == platform.node()
    assert environment.working_directory == os.getcwd()
    assert environment.process_id == os.getpid()
    assert environment.executable == os.path.abspath(os.sys.executable)

def test_runtime_state():
    state = RuntimeState(
        status="running",
        environment_type="development",
    )

    assert state.status == "running"
    assert state.environment_type == "development"
