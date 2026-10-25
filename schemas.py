"""Pydantic request/response schemas (the API contract)."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator

NonBlank = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=60)]
CURRENT_YEAR_CEILING = 2100


# ---------- Auth ----------


class RegisterRequest(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def _lowercase_email(cls, value: str) -> str:
        return value.lower()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def _lowercase_email(cls, value: str) -> str:
        return value.lower()


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    is_admin: bool


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Vehicles ----------


class VehicleBase(BaseModel):
    year: int | None = Field(default=None, ge=1886, le=CURRENT_YEAR_CEILING)
    color: Annotated[str, StringConstraints(strip_whitespace=True, max_length=40)] | None = None
    image_url: Annotated[str, StringConstraints(strip_whitespace=True, max_length=500)] | None = None
    description: Annotated[str, StringConstraints(strip_whitespace=True, max_length=2000)] | None = None


class VehicleCreate(VehicleBase):
    make: NonBlank
    model: NonBlank
    category: NonBlank
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class VehicleUpdate(VehicleBase):
    """All fields optional: only supplied fields are changed (partial update)."""

    make: NonBlank | None = None
    model: NonBlank | None = None
    category: NonBlank | None = None
    price: float | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)


class VehicleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    make: str
    model: str
    category: str
    price: float
    quantity: int
    year: int | None = None
    color: str | None = None
    image_url: str | None = None
    description: str | None = None


class VehicleSearchParams(BaseModel):
    make: str | None = None
    model: str | None = None
    category: str | None = None
    min_price: float | None = Field(default=None, ge=0)
    max_price: float | None = Field(default=None, ge=0)


class QuantityRequest(BaseModel):
    quantity: int = Field(default=1, ge=1, le=10_000)


class RestockRequest(BaseModel):
    quantity: int = Field(ge=1, le=10_000)
