from app.models import Article


def test_search_get_1(client):
    response = client.get("/search", follow_redirects=True)
    assert response.status_code == 200
    assert response.status_code != 302
    assert "predam" in str(response.data)


def test_search_query_1(client):
    response = client.post(
        "/search",
        data={"article_text": "*"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert 'Sorry, no matches found for : "*"' in str(response.data)


def test_search_query_2(client):
    response = client.post(
        "/search",
        data={"article_text": "predam"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert 'predam' in str(response.data)
