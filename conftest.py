"""Shared pytest fixtures.

Every test gets a brand-new SQLite database file in a temporary directory,
so tests are isolated from each other and from the developer's local DB.
"""

from collections.abc import Callable, Iterator

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app

ADMIN_EMAIL = "admin@example.com"


@pytest.fixture
def settings(tmp_path) -> Settings:
    return Settings(
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        jwt_secret="test-secret-key-that-is-long-enough-for-hs256",
        jwt_expire_minutes=30,
        bcrypt_rounds=4,  # minimum work factor keeps the suite fast
        admin_emails=(ADMIN_EMAIL,),
        cors_origins=("http://localhost:5173",),
    )


@pytest.fixture
def client(settings) -> Iterator[TestClient]:
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client


def _register_and_login(client: TestClient, email: str, name: str = "Test User") -> str:
    password = "Str0ngPass!"
    client.post("/api/auth/register", json={"name": name, "email": email, "password": password})
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


@pytest.fixture
def user_headers(client) -> dict[str, str]:
    token = _register_and_login(client, "buyer@example.com", "Regular Buyer")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client) -> dict[str, str]:
    token = _register_and_login(client, ADMIN_EMAIL, "Admin")
    return {"Authorization": f"Bearer {token}"}


VehiclePayload = dict[str, object]


@pytest.fixture
def vehicle_payload() -> VehiclePayload:
    return {
        "make": "Toyota",
        "model": "Corolla",
        "category": "Sedan",
        "price": 21500.0,
        "quantity": 5,
        "year": 2024,
    }


@pytest.fixture
def create_vehicle(client, admin_headers, vehicle_payload) -> Callable[..., dict]:
    """Factory fixture: create a vehicle as admin, overriding any fields."""

    def _create(**overrides) -> dict:
        payload = {**vehicle_payload, **overrides}
        response = client.post("/api/vehicles", json=payload, headers=admin_headers)
        assert response.status_code == 201, response.text
        return response.json()

    return _create
