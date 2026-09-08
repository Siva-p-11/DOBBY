import hashlib
import hmac
from pathlib import Path


class AuthenticationSetup:
    """Initialize the stored authentication-key hash."""

    def __init__(self, key_path: str | Path) -> None:
        self._key_path = Path(key_path)

    def initialize(self, key: str) -> None:
        """Store a hash of the supplied authentication key."""

        if not key:
            raise ValueError("Authentication key cannot be empty.")

        key_hash = hashlib.sha256(
            key.encode("utf-8")
        ).hexdigest()

        self._key_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._key_path.write_text(
            key_hash,
            encoding="utf-8",
        )

        try:
            self._key_path.chmod(0o600)
        except PermissionError:
            pass

    def verify(self, key: str) -> bool:
        """Verify a key against the stored key hash."""

        if not self._key_path.exists():
            return False

        stored_hash = self._key_path.read_text(
            encoding="utf-8"
        ).strip()

        entered_hash = hashlib.sha256(
            key.encode("utf-8")
        ).hexdigest()

        return hmac.compare_digest(
            entered_hash,
            stored_hash,
        )
