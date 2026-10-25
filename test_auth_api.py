"""API tests for /api/auth/register and /api/auth/login."""

REGISTER = "/api/auth/register"
LOGIN = "/api/auth/login"
ME = "/api/auth/me"


def _register(client, email="jane@example.com", password="Str0ngPass!", name="Jane Doe"):
    return client.post(REGISTER, json={"name": name, "email": email, "password": password})


class TestRegister:
    def test_register_returns_201_with_user_and_token(self, client):
        response = _register(client)
        assert response.status_code == 201
        body = response.json()
        assert body["user"]["email"] == "jane@example.com"
        assert body["user"]["is_admin"] is False
        assert body["access_token"]
        assert body["token_type"] == "bearer"

    def test_register_never_returns_password_or_hash(self, client):
        body = _register(client).json()
        assert "password" not in body["user"]
        assert "password_hash" not in body["user"]

    def test_register_normalises_email_case(self, client):
        body = _register(client, email="Jane@Example.COM").json()
        assert body["user"]["email"] == "jane@example.com"

    def test_duplicate_email_returns_409(self, client):
        _register(client)
        response = _register(client, email="JANE@example.com")
        assert response.status_code == 409

    def test_short_password_returns_422(self, client):
        assert _register(client, password="short").status_code == 422

    def test_invalid_email_returns_422(self, client):
        assert _register(client, email="not-an-email").status_code == 422

    def test_blank_name_returns_422(self, client):
        assert _register(client, name="   ").status_code == 422

    def test_configured_admin_email_registers_as_admin(self, client):
        body = _register(client, email="admin@example.com").json()
        assert body["user"]["is_admin"] is True


class TestLogin:
    def test_login_with_valid_credentials_returns_token(self, client):
        _register(client)
        response = client.post(LOGIN, json={"email": "jane@example.com", "password": "Str0ngPass!"})
        assert response.status_code == 200
        assert response.json()["access_token"]

    def test_login_with_wrong_password_returns_401(self, client):
        _register(client)
        response = client.post(LOGIN, json={"email": "jane@example.com", "password": "WrongPass!"})
        assert response.status_code == 401

    def test_login_with_unknown_email_returns_401(self, client):
        response = client.post(LOGIN, json={"email": "ghost@example.com", "password": "Whatever1!"})
        assert response.status_code == 401

    def test_login_error_message_does_not_reveal_which_field_was_wrong(self, client):
        _register(client)
        wrong_pass = client.post(LOGIN, json={"email": "jane@example.com", "password": "nope-nope"})
        no_user = client.post(LOGIN, json={"email": "ghost@example.com", "password": "nope-nope"})
        assert wrong_pass.json()["detail"] == no_user.json()["detail"]


class TestCurrentUser:
    def test_me_returns_current_user(self, client, user_headers):
        response = client.get(ME, headers=user_headers)
        assert response.status_code == 200
        assert response.json()["email"] == "buyer@example.com"

    def test_me_without_token_returns_401(self, client):
        assert client.get(ME).status_code == 401

    def test_me_with_invalid_token_returns_401(self, client):
        response = client.get(ME, headers={"Authorization": "Bearer garbage"})
        assert response.status_code == 401

    def test_token_for_user_that_no_longer_exists_returns_401(self, client, settings):
        from app.core.security import TokenService

        token = TokenService(settings.jwt_secret, 5).create_access_token(subject="99999")
        response = client.get(ME, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 401
