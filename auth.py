"""Auth endpoints: register, login, current user."""

from fastapi import APIRouter, status

from app.dependencies import AuthServiceDep, CurrentUser
from app.schemas import AuthResponse, LoginRequest, RegisterRequest, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _auth_response(user, token: str) -> AuthResponse:
    return AuthResponse(access_token=token, user=UserOut.model_validate(user))


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, auth: AuthServiceDep) -> AuthResponse:
    """Create an account and return an access token so the user is logged in immediately."""
    return _auth_response(*auth.register(payload))


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, auth: AuthServiceDep) -> AuthResponse:
    return _auth_response(*auth.login(payload))


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser) -> UserOut:
    return UserOut.model_validate(user)
