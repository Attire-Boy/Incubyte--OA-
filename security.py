"""Password hashing (bcrypt) and JWT access tokens (HS256)."""

from datetime import UTC, datetime, timedelta

import bcrypt
import jwt


class InvalidTokenError(Exception):
    """Raised when a token is malformed, expired or has a bad signature."""


class PasswordHasher:
    """Hashes and verifies passwords with bcrypt (salted, slow by design).

    ``rounds`` is the bcrypt work factor; tests lower it to stay fast.
    """

    def __init__(self, rounds: int = 12) -> None:
        self._rounds = rounds

    def hash(self, password: str) -> str:
        salt = bcrypt.gensalt(rounds=self._rounds)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify(self, password: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        except ValueError:
            return False


class TokenService:
    """Issues and validates signed JWT access tokens."""

    ALGORITHM = "HS256"

    def __init__(self, secret: str, expire_minutes: int) -> None:
        self._secret = secret
        self._default_ttl = timedelta(minutes=expire_minutes)

    def create_access_token(self, subject: str, expires_delta: timedelta | None = None) -> str:
        now = datetime.now(UTC)
        payload = {"sub": subject, "iat": now, "exp": now + (expires_delta or self._default_ttl)}
        return jwt.encode(payload, self._secret, algorithm=self.ALGORITHM)

    def decode_subject(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self.ALGORITHM])
        except jwt.PyJWTError as exc:
            raise InvalidTokenError(str(exc)) from exc
        subject = payload.get("sub")
        if not subject:
            raise InvalidTokenError("Token has no subject")
        return subject
