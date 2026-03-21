import os
import pytest
from fastapi.testclient import TestClient
from main import app
from jose import jwt
from datetime import datetime, timedelta

client = TestClient(app)

# --- Helpers ---

def make_jwt_token(secret, username="admin", exp_minutes=60):
    now = datetime.utcnow()
    payload = {
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=exp_minutes)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm="HS256")

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "password123")
    monkeypatch.setenv("JWT_SECRET", "supersecretjwt")
    yield

# --- R1: Login Endpoint ---
def test_login_success_returns_jwt():
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "password123"})
    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    # Validate JWT structure
    decoded = jwt.decode(data["token"], os.environ["JWT_SECRET"], algorithms=["HS256"])
    assert decoded["sub"] == "admin"
    assert "exp" in decoded

def test_login_invalid_credentials_returns_401():
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "wrongpass"})
    assert resp.status_code == 401
    assert "token" not in resp.json()

# --- R2: Token Validation Endpoint ---
def test_me_with_valid_token_returns_authenticated():
    token = make_jwt_token(os.environ["JWT_SECRET"], "admin")
    resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json() == {"authenticated": True}

def test_me_with_invalid_token_returns_401():
    # Invalid token
    resp = client.get("/api/auth/me", headers={"Authorization": "Bearer invalidtoken"})
    assert resp.status_code == 401

def test_me_with_missing_token_returns_401():
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401

def test_login_missing_env_vars_returns_401(monkeypatch):
    monkeypatch.delenv("ADMIN_USERNAME", raising=False)
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)
    monkeypatch.delenv("JWT_SECRET", raising=False)
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "password123"})
    assert resp.status_code == 401

def test_login_with_malformed_json_returns_422():
    resp = client.post("/api/auth/login", data="notjson", headers={"Content-Type": "application/json"})
    assert resp.status_code == 422

def test_me_with_expired_token_returns_401():
    token = make_jwt_token(os.environ["JWT_SECRET"], "admin", exp_minutes=-1)
    resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401
