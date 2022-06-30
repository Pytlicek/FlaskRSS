from app.models import Article

number_of_articles = 0


def test_feed_get_1(client):
    response = client.get("/feeds/download/")
    assert response.status_code == 200
    assert response.status_code != 302


# def test_no_of_articles_1():
#     articles = Article.get_all_articles()
#     assert len(articles) > 0


def test_feed_delete_1(client):
    response = client.get("/feeds/1/delete")
    assert response.status_code != 200
    assert response.status_code == 302
    assert "/feeds" in response.headers["location"]


def test_no_of_articles_2():
    articles = Article.get_all_articles()
    assert len(articles) == 0


def test_feed_add_2(client):
    response = client.post(
        "/feeds",
        data={
            "name": "feed2",
            "url": "https://www.thepoke.co.uk/category/news/feed/",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "feed2" in str(response.data)
    assert "https://www.thepoke.co.uk/category/news/feed/" in str(
        response.data
    )


def test_feed_get_3(client):
    response = client.get("/feeds/download/1")
    assert response.status_code == 200
    assert response.status_code != 302


def test_no_of_articles_4():
    global number_of_articles
    articles = Article.get_all_articles()
    assert len(articles) > 0
    assert len(articles) > number_of_articles


def test_delete_articles_by_feed_id_1():
    global number_of_articles
    result = Article.delete_articles_by_feed_id(1)
    assert result is True
    articles = Article.get_all_articles()
    assert len(articles) == number_of_articles
