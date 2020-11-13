def test_feed_get_1(client):
    response = client.get("/feeds")
    assert response.status_code == 200
    assert response.status_code != 302
    assert "Add New feed" in str(response.data)


def test_feed_post(client):
    response = client.post(
        "/feeds",
        data={"name": "feed1", "url": "https://www.bazos.sk/rss.php"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "feed1" in str(response.data)
    assert "https://www.bazos.sk/rss.php" in str(response.data)


def test_feed_post_2(client):
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


def test_feed_edit_1(client):
    response = client.post(
        "/feeds/edit/2",
        data={"name": "feed2", "url": "https://www.feed2/feed/"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "feed2" in str(response.data)
    assert "https://www.feed2/feed/" in str(response.data)
    assert "https://www.thepoke.co.uk/category/news/feed/" not in str(
        response.data
    )


def test_feed_delete_1(client):
    response = client.get("/feeds/3/delete")
    assert response.status_code != 200
    assert response.status_code == 302
    assert "/feeds" in response.headers["location"]


def test_feed_delete_2(client):
    response = client.get("/feeds/2/delete")
    assert response.status_code != 200
    assert response.status_code == 302
    assert "/feeds" in response.headers["location"]


def test_feed_get_2(client):
    response = client.get("/feeds")
    assert response.status_code == 200
    assert response.status_code != 302
    assert "feed1" in str(response.data)
    assert "feed2" not in str(response.data)


def test_feed_edit_2(client):
    response = client.post(
        "/feeds/edit/1",
        data={"name": "feed_1", "url": "https://www.bazos.sk/rss.php"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "feed_1" in str(response.data)
    assert "feed1" not in str(response.data)
    assert "https://www.bazos.sk/rss.php" in str(response.data)
