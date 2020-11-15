from flask import url_for
from app import app


def test_index_path(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert response.status_code != 302
    assert "Login" in str(response.data)
    assert "Articles:" not in str(response.data)


def test_feed_path_unauthorized(client):
    response = client.get("/feeds")
    assert response.status_code != 200
    assert response.status_code == 302
    assert "Redirecting..." in str(response.data)


def test_search_get_unauthorized(client):
    response = client.get("/search", follow_redirects=True)
    assert response.status_code == 200
    assert response.status_code != 302
    assert "predam" not in str(response.data)
