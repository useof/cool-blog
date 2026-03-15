import pytest
from fastapi.testclient import TestClient
from main import app

import pytest

client = TestClient(app)

# Fixtures for mock authentication and DB
def auth_headers():
    return {"Authorization": "Bearer testtoken"}

# --- GET /api/posts (pagination, public) ---
def test_get_posts_returns_paginated_list():
    response = client.get("/api/posts?page=1")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) <= 10
    assert "total" in data
    assert "page" in data
    assert data["page"] == 1

def test_get_posts_filters_published_only():
    response = client.get("/api/posts")
    assert response.status_code == 200
    for post in response.json()["items"]:
        assert post["status"] == "published"

# --- GET /api/posts/{id} (public) ---
def test_get_post_by_id_returns_post():
    response = client.get("/api/posts/1")
    assert response.status_code == 200
    post = response.json()
    assert "id" in post and post["id"] == 1
    assert "title" in post
    assert "content" in post

# --- POST /api/posts (protected) ---
def test_create_post_requires_auth():
    response = client.post("/api/posts", json={"title": "New Post", "content": "Body"})
    assert response.status_code == 401

def test_create_post_success():
    response = client.post(
        "/api/posts",
        json={"title": "New Post", "content": "Body", "status": "draft"},
        headers=auth_headers(),
    )
    assert response.status_code == 201
    post = response.json()
    assert post["title"] == "New Post"
    assert post["status"] == "draft"

# --- PUT /api/posts/{id} (protected) ---
def test_update_post_requires_auth():
    response = client.put("/api/posts/1", json={"title": "Updated"})
    assert response.status_code == 401

def test_update_post_success():
    response = client.put(
        "/api/posts/1",
        json={"title": "Updated Title", "content": "Updated Body", "status": "published"},
        headers=auth_headers(),
    )
    assert response.status_code == 200
    post = response.json()
    assert post["title"] == "Updated Title"
    assert post["status"] == "published"

# --- DELETE /api/posts/{id} (protected) ---
def test_delete_post_requires_auth():
    response = client.delete("/api/posts/1")
    assert response.status_code == 401

def test_delete_post_success():
    response = client.delete("/api/posts/1", headers=auth_headers())
    assert response.status_code == 204

# --- Error/edge cases ---
def test_get_post_not_found():
    response = client.get("/api/posts/9999")
    assert response.status_code == 404

def test_update_post_not_found():
    response = client.put("/api/posts/9999", json={"title": "X"}, headers=auth_headers())
    assert response.status_code == 404

def test_delete_post_not_found():
    response = client.delete("/api/posts/9999", headers=auth_headers())
    assert response.status_code == 404

# --- Validation ---
def test_create_post_invalid_payload():
    response = client.post("/api/posts", json={"title": ""}, headers=auth_headers())
    assert response.status_code == 422

def test_update_post_invalid_payload():
    response = client.put("/api/posts/1", json={"title": ""}, headers=auth_headers())
    assert response.status_code == 422
