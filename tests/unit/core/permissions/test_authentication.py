from pathlib import Path

import pytest

from dobby.core.permissions.authentication import (
    AuthenticationSetup,
    KeyAuthenticationAuthority,
)
from dobby.core.permissions.risk import PolicyRiskLevel


def test_initialize_stores_hashed_key(tmp_path: Path) -> None:
    key_path = tmp_path / "auth" / "credential"

    setup = AuthenticationSetup(key_path)
    setup.initialize("test-secret")

    assert key_path.exists()
    assert key_path.read_text(encoding="utf-8") != "test-secret"


def test_empty_key_is_rejected(tmp_path: Path) -> None:
    key_path = tmp_path / "credential"

    setup = AuthenticationSetup(key_path)

    with pytest.raises(ValueError):
        setup.initialize("")


def test_verify_correct_key(tmp_path: Path) -> None:
    key_path = tmp_path / "credential"

    setup = AuthenticationSetup(key_path)
    setup.initialize("test-secret")

    assert setup.verify("test-secret") is True


def test_verify_wrong_key(tmp_path: Path) -> None:
    key_path = tmp_path / "credential"

    setup = AuthenticationSetup(key_path)
    setup.initialize("test-secret")

    assert setup.verify("wrong-secret") is False


def test_missing_key_returns_false(tmp_path: Path) -> None:
    key_path = tmp_path / "credential"

    setup = AuthenticationSetup(key_path)

    assert setup.verify("test-secret") is False


def test_authority_can_be_created(tmp_path: Path) -> None:
    key_path = tmp_path / "credential"

    setup = AuthenticationSetup(key_path)
    setup.initialize("test-secret")

    authority = KeyAuthenticationAuthority(key_path)

    assert authority is not None
