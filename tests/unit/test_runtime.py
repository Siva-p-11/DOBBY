import platform

from dobby.core.runtime import RuntimeIdentity


def test_runtime_identity():
    identity = RuntimeIdentity.create(
        name="dobby",
        environment="development",
    )

    assert identity.name == "dobby"
    assert identity.version == "0.1.0"
    assert identity.environment == "development"
    assert identity.python_version == platform.python_version()
