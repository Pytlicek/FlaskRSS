from flask import url_for
from app import app


def test_index_path(client):
    response = client.get("login", follow_redirects=True)
    assert response.status_code == 200
    assert response.status_code != 302
    assert "Login" in str(response.data)
    assert "Articles:" not in str(response.data)


def test_feed_path_unauthorized(client):
    response = client.get("/feeds")
    assert response.status_code != 200
    assert response.status_code == 302
    assert "Redirecting..." in str(response.data)


def test_login_path(client):
    response = client.get("/login", follow_redirects=True)
    assert response.status_code == 200

    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=True,
    )
    assert "Articles:" in str(response.data)
    assert "No articles found" in str(response.data)
    assert "Sign out admin" in str(response.data)
