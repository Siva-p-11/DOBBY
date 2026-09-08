from abc import ABC, abstractmethod
import getpass
import hashlib
import hmac
from pathlib import Path

from dobby.core.permissions.risk import PolicyRiskLevel


class AuthenticationAuthority(ABC):
    """Trusted authority responsible for approving protected actions."""

    @abstractmethod
    def authenticate(self, risk_level: PolicyRiskLevel) -> bool:
        """Authenticate an action requiring the specified risk level."""
        raise NotImplementedError


class KeyAuthenticationAuthority(AuthenticationAuthority):
    """Authenticate protected actions using a user-controlled secret key."""

    def __init__(self, key_path: str | Path) -> None:
        self._key_path = Path(key_path)

    def authenticate(self, risk_level: PolicyRiskLevel) -> bool:
        """
        Request the user's authentication key and verify it.

        The plaintext key is never returned to the caller.
        """

        stored_hash = self._load_key_hash()

        entered_key = getpass.getpass(
            f"Authentication required ({risk_level.name}). Enter key: "
        )

        entered_hash = hashlib.sha256(
            entered_key.encode("utf-8")
        ).hexdigest()

        return hmac.compare_digest(entered_hash, stored_hash)

    def _load_key_hash(self) -> str:
        """Load the stored authentication-key hash."""

        if not self._key_path.exists():
            raise FileNotFoundError(
                "Authentication key configuration does not exist."
            )

        stored_hash = self._key_path.read_text(
            encoding="utf-8"
        ).strip()

        if not stored_hash:
            raise ValueError(
                "Authentication key configuration is empty."
            )

        return stored_hash
