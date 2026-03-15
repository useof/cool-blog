import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

# --- Fixtures and helpers ---

def auth_headers(user_type="user"):
    # Simulate auth headers for user or admin
    token = "user-token" if user_type == "user" else "admin-token"
    return {"Authorization": f"Bearer {token}"}

# --- Test: GET /api/posts (pagination, public) ---
def test_get_posts_pagination_returns_paginated_posts():
    with patch("database.get_posts_paginated") as mock_get_posts:
        mock_get_posts.return_value = ([{"id": 1, "title": "Post 1", "status": "published"}], 10)
        response = client.get("/api/posts?page=1&size=1")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data and len(data["items"]) == 1
        assert data["total"] == 10

# --- Test: GET /api/posts/{id} (public) ---
def test_get_post_by_id_returns_post():
    with patch("database.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = {"id": 1, "title": "Post 1", "status": "published"}
        response = client.get("/api/posts/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

def test_get_post_by_id_not_found_returns_404():
    with patch("database.get_post_by_id") as mock_get_post:
        mock_get_post.return_value = None
        response = client.get("/api/posts/999")
        assert response.status_code == 404

# --- Test: POST /api/posts (admin only) ---
def test_create_post_requires_auth():
    response = client.post("/api/posts", json={"title": "New Post", "content": "..."})
    assert response.status_code == 401

def test_create_post_admin_creates_post():
    with patch("database.create_post") as mock_create_post:
        mock_create_post.return_value = {"id": 2, "title": "New Post", "status": "draft"}
        response = client.post(
            "/api/posts",
            json={"title": "New Post", "content": "..."},
            headers=auth_headers("admin")
        )
        assert response.status_code == 201
        assert response.json()["id"] == 2

# --- Test: PUT /api/posts/{id} (admin only) ---
def test_update_post_requires_auth():
    response = client.put("/api/posts/1", json={"title": "Updated"})
    assert response.status_code == 401

def test_update_post_admin_updates_post():
    with patch("database.update_post") as mock_update_post:
        mock_update_post.return_value = {"id": 1, "title": "Updated", "status": "published"}
        response = client.put(
            "/api/posts/1",
            json={"title": "Updated"},
            headers=auth_headers("admin")
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated"

def test_update_post_not_found_returns_404():
    with patch("database.update_post") as mock_update_post:
        mock_update_post.return_value = None
        response = client.put(
            "/api/posts/999",
            json={"title": "Updated"},
            headers=auth_headers("admin")
        )
        assert response.status_code == 404

# --- Test: DELETE /api/posts/{id} (admin only) ---
def test_delete_post_requires_auth():
    response = client.delete("/api/posts/1")
    assert response.status_code == 401

def test_delete_post_admin_deletes_post():
    with patch("database.delete_post") as mock_delete_post:
        mock_delete_post.return_value = True
        response = client.delete("/api/posts/1", headers=auth_headers("admin"))
        assert response.status_code == 204

def test_delete_post_not_found_returns_404():
    with patch("database.delete_post") as mock_delete_post:
        mock_delete_post.return_value = False
        response = client.delete("/api/posts/999", headers=auth_headers("admin"))
        assert response.status_code == 404

# --- Test: Only published posts are public ---
def test_get_posts_only_returns_published():
    with patch("database.get_posts_paginated") as mock_get_posts:
        mock_get_posts.return_value = ([{"id": 1, "title": "Post 1", "status": "draft"}], 1)
        response = client.get("/api/posts")
        # Should not return draft posts to public
        assert response.status_code == 200
        assert all(post["status"] == "published" for post in response.json().get("items", []))
