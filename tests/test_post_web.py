import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_auth_headers():
    # This should be replaced with a real login if needed
    return {"Authorization": "Bearer user-token"}

def test_create_post_form_shows_for_authenticated_user():
    response = client.get("/posts/new", headers=get_auth_headers())
    assert response.status_code == 200
    assert "form" in response.text.lower()
    assert "title" in response.text.lower()
    assert "content" in response.text.lower()

def test_create_post_success_and_redirect():
    # Simulate form submission
    data = {"title": "My First Post", "content": "Hello world!"}
    response = client.post("/posts/new", data=data, headers=get_auth_headers(), allow_redirects=False)
    assert response.status_code in (302, 303)
    assert "/posts/mine" in response.headers["location"]

def test_create_post_invalid_submission():
    # Missing title
    data = {"title": "", "content": "No title"}
    response = client.post("/posts/new", data=data, headers=get_auth_headers())
    assert response.status_code == 400
    assert "required" in response.text.lower() or "error" in response.text.lower()

def test_my_posts_page_shows_user_posts():
    # This test assumes the user has at least one post after creation
    response = client.get("/posts/mine", headers=get_auth_headers())
    assert response.status_code == 200
    assert "my first post" in response.text.lower()
    assert "hello world" in response.text.lower()

def test_my_posts_page_ordering():
    # Create two posts and check order
    client.post("/posts/new", data={"title": "Older Post", "content": "Old"}, headers=get_auth_headers())
    client.post("/posts/new", data={"title": "Newer Post", "content": "New"}, headers=get_auth_headers())
    response = client.get("/posts/mine", headers=get_auth_headers())
    assert response.status_code == 200
    # Newer post should appear before older post
    text = response.text.lower()
    assert text.index("newer post") < text.index("older post")

def test_my_posts_page_only_shows_current_user_posts():
    # This test assumes isolation or mocking of user context
    response = client.get("/posts/mine", headers=get_auth_headers())
    assert response.status_code == 200
    # Should not show posts from other users
    assert "other user's post" not in response.text.lower()
