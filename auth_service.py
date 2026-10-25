"""Registration, login and token-to-user resolution."""

from app.core.exceptions import AuthenticationError, ConflictError
from app.core.security import InvalidTokenError, PasswordHasher, TokenService
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas import LoginRequest, RegisterRequest

INVALID_CREDENTIALS = "Invalid email or password"


class AuthService:
    def __init__(
        self,
        users: UserRepository,
        hasher: PasswordHasher,
        tokens: TokenService,
        admin_emails: tuple[str, ...] = (),
    ) -> None:
        self._users = users
        self._hasher = hasher
        self._tokens = tokens
        self._admin_emails = {email.lower() for email in admin_emails}

    def register(self, data: RegisterRequest) -> tuple[User, str]:
        if self._users.get_by_email(data.email):
            raise ConflictError("An account with this email already exists")
        user = self._users.add(
            User(
                name=data.name,
                email=data.email,
                password_hash=self._hasher.hash(data.password),
                is_admin=data.email in self._admin_emails,
            )
        )
        return user, self._issue_token(user)

    def login(self, data: LoginRequest) -> tuple[User, str]:
        user = self._users.get_by_email(data.email)
        # Same message for unknown email and wrong password: don't leak which accounts exist.
        if user is None or not self._hasher.verify(data.password, user.password_hash):
            raise AuthenticationError(INVALID_CREDENTIALS)
        return user, self._issue_token(user)

    def user_from_token(self, token: str) -> User:
        try:
            user_id = int(self._tokens.decode_subject(token))
        except (InvalidTokenError, ValueError) as exc:
            raise AuthenticationError("Invalid or expired token") from exc
        user = self._users.get_by_id(user_id)
        if user is None:
            raise AuthenticationError("Invalid or expired token")
        return user

    def _issue_token(self, user: User) -> str:
        return self._tokens.create_access_token(subject=str(user.id))
