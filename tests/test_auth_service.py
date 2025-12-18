from src.services.auth_service import AuthService
import uuid

def test_register_success():
    auth = AuthService()

    username = f"user_{uuid.uuid4().hex[:8]}"
    email = f"{username}@test.com"

    result = auth.register(
        username=username,
        password="abc123",
        email=email,
        campus="主校区"
    )
    assert result["success"] is True


def test_register_empty_field():
    auth = AuthService()
    result = auth.register("", "abc123", "a@b.com", "主校区")
    assert result["success"] is False

def test_register_invalid_username():
    auth = AuthService()
    result = auth.register("ab", "abc123", "a@b.com", "主校区")
    assert result["success"] is False

def test_register_invalid_email():
    auth = AuthService()
    result = auth.register("user123", "abc123", "invalid", "主校区")
    assert result["success"] is False

def test_register_invalid_password():
    auth = AuthService()
    result = auth.register("user123", "123", "a@b.com", "主校区")
    assert result["success"] is False

def test_login_success():
    auth = AuthService()
    auth.register("user1", "abc123", "u1@test.com", "主校区")
    result = auth.login("user1", "abc123")
    assert result["success"] is True

def test_login_wrong_password():
    auth = AuthService()
    auth.register("user2", "abc123", "u2@test.com", "主校区")
    result = auth.login("user2", "wrong")
    assert result["success"] is False

def test_login_nonexistent_user():
    auth = AuthService()
    result = auth.login("nouser", "abc123")
    assert result["success"] is False

def test_logout():
    auth = AuthService()
    auth.logout()
    assert auth.is_logged_in() is False

def test_get_current_user():
    auth = AuthService()
    auth.register("user3", "abc123", "u3@test.com", "主校区")
    auth.login("user3", "abc123")
    assert auth.get_current_user() is not None
