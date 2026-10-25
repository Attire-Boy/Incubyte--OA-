"""Unit tests for password hashing and JWT token handling."""

from datetime import timedelta

import pytest

from app.core.security import InvalidTokenError, PasswordHasher, TokenService

SECRET = "unit-test-secret-key-that-is-long-enough"


class TestPasswordHasher:
    def test_hash_is_not_the_plain_password(self):
        hasher = PasswordHasher(rounds=4)
        assert hasher.hash("s3cret-pass") != "s3cret-pass"

    def test_verify_accepts_correct_password(self):
        hasher = PasswordHasher(rounds=4)
        hashed = hasher.hash("s3cret-pass")
        assert hasher.verify("s3cret-pass", hashed) is True

    def test_verify_rejects_wrong_password(self):
        hasher = PasswordHasher(rounds=4)
        hashed = hasher.hash("s3cret-pass")
        assert hasher.verify("wrong-pass", hashed) is False

    def test_same_password_produces_different_hashes(self):
        hasher = PasswordHasher(rounds=4)
        assert hasher.hash("same") != hasher.hash("same")


class TestTokenService:
    def test_round_trip_returns_subject(self):
        tokens = TokenService(secret=SECRET, expire_minutes=5)
        token = tokens.create_access_token(subject="42")
        assert tokens.decode_subject(token) == "42"

    def test_expired_token_is_rejected(self):
        tokens = TokenService(secret=SECRET, expire_minutes=5)
        token = tokens.create_access_token(subject="42", expires_delta=timedelta(seconds=-1))
        with pytest.raises(InvalidTokenError):
            tokens.decode_subject(token)

    def test_token_signed_with_other_secret_is_rejected(self):
        issuer = TokenService(secret=SECRET, expire_minutes=5)
        verifier = TokenService(secret=SECRET + "-different", expire_minutes=5)
        token = issuer.create_access_token(subject="42")
        with pytest.raises(InvalidTokenError):
            verifier.decode_subject(token)

    def test_garbage_token_is_rejected(self):
        tokens = TokenService(secret=SECRET, expire_minutes=5)
        with pytest.raises(InvalidTokenError):
            tokens.decode_subject("not-a-jwt")
