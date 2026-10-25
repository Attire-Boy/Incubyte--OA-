"""FastAPI dependency providers (composition root for each request)."""

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError, PermissionDeniedError
from app.core.security import PasswordHasher, TokenService
from app.models import User
from app.repositories.user_repository import UserRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.services.auth_service import AuthService
from app.services.vehicle_service import VehicleService

_bearer = HTTPBearer(auto_error=False)


def get_session(request: Request) -> Iterator[Session]:
    session = request.app.state.database.new_session()
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]


def get_auth_service(request: Request, session: SessionDep) -> AuthService:
    settings = request.app.state.settings
    return AuthService(
        users=UserRepository(session),
        hasher=PasswordHasher(settings.bcrypt_rounds),
        tokens=TokenService(settings.jwt_secret, settings.jwt_expire_minutes),
        admin_emails=settings.admin_emails,
    )


def get_vehicle_service(session: SessionDep) -> VehicleService:
    return VehicleService(VehicleRepository(session))


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
VehicleServiceDep = Annotated[VehicleService, Depends(get_vehicle_service)]


def get_current_user(
    auth: AuthServiceDep,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError("Not authenticated")
    return auth.user_from_token(credentials.credentials)


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_admin(user: CurrentUser) -> User:
    if not user.is_admin:
        raise PermissionDeniedError("Admin privileges required")
    return user


AdminUser = Annotated[User, Depends(require_admin)]
