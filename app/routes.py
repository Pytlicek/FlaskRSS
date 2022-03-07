from flask import url_for, redirect, flash, request
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
)

from app import app
from app.forms import LoginForm, AddFeedForm, SearchForm
from app.helpers import templated
from app.models import User, Feed, Article, download_articles

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return redirect(url_for("items_index"))


@app.route("/login", methods=["GET", "POST"])
@templated()
def login():
    form = LoginForm()
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
        login_user(user)
        return redirect(url_for("index"))
    return dict(form=LoginForm())


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/feeds", methods=["GET", "POST"])
@login_required
@templated()
def feeds_index():
    form = AddFeedForm()
    if AddFeedForm().validate_on_submit():
        Feed.add_feed(form.data["name"], form.data["url"])
        flash("Feed has been added", "success")
    return dict(feeds=Feed.get_all_feeds(), form=form)


@app.route("/feeds/edit/<feed_id>", methods=["GET", "POST"])
@login_required
@templated()
def feeds_edit(feed_id):
    form = AddFeedForm()
    if form.validate_on_submit():
        Feed.edit_feed(feed_id, form.data["name"], form.data["url"])
        flash("Feed has been changed", "success")
        return redirect(url_for("feeds_index"))

    feed_data = Feed.get_feed_by_id(feed_id)
    if not feed_data:
        return redirect(url_for("feeds_index"))
    feed_data = feed_data[0]
    return dict(form=form, feed_data=feed_data)


@app.route("/feeds/<feed_id>/delete", methods=["GET"])
@login_required
def feeds_delete(feed_id):
    if Feed.delete_feed(feed_id) is True:
        flash("Feed has been deleted", "success")
    return redirect(url_for("feeds_index"))


@app.route("/feeds/download/", defaults={"feed_id": None}, methods=["GET"])
@app.route("/feeds/download/<feed_id>")
@login_required
@templated()
def feeds_download(feed_id):
    if feed_id is None or feed_id == "all":
        feeds = Feed.get_all_feeds()
        print(feeds)
    else:
        feeds = Feed.get_feed_by_id(feed_id)

    articles_list = []
    for feed in feeds:
        articles = download_articles(feed.url, feed.id)
        articles_list += articles
    if feed_id != "all":
        return dict(articles_list=articles_list)
    else:
        return "".join(articles_list)


@app.route("/feeds/refresh", methods=["GET"])
def feeds_refresh():
    import time
    feeds = Feed.get_all_feeds()
    articles_list = []
    for feed in feeds:
        print("Refreshing feed:", feed.id, feed.url)
        articles = download_articles(feed.url, feed.id)
        time.sleep(10)
        articles_list += articles

    return "".join(articles_list)


@app.route("/feeds/articles", defaults={"feed_id": None}, methods=["GET"])
@app.route("/feeds/<feed_id>/articles/")
@login_required
@templated("articles_index.html")
def feeds_articles(feed_id):
    if feed_id is None:
        articles = Article.get_last_articles()
    else:
        articles = Article.get_articles_by_feed_id(feed_id)
    return dict(articles=articles, feeds=Feed.get_all_feeds())


@app.route("/search", methods=["GET", "POST"])
@login_required
@templated("articles_index.html")
def search():
    if request.method == "POST":
        form = SearchForm()
        search_query = form.data["article_text"]
        articles = Article.query.filter(
            Article.summary.ilike(f"%{search_query}%")
        ).all()
    else:
        search_query = False
        articles = Article.get_all_articles()

    return dict(articles=articles, search_query=search_query)


@app.route("/items", defaults={"feed_id": None}, methods=["GET"])
@app.route("/items/<feed_id>/")
@templated("items_index.html")
def items_index(feed_id):
    if feed_id is None:
        articles = Article.get_last_articles()
        feed_name = "All"
    else:
        feed_name = Feed.get_feed_by_id(feed_id)[0].name
        articles = Article.get_articles_by_feed_id(feed_id)
    return dict(articles=articles, feeds=Feed.get_all_feeds(), feed_name=feed_name)


@app.route("/items-search", methods=["GET", "POST"])
@templated("items_index.html")
def items_search():
    if request.method == "POST":
        form = SearchForm()
        search_query = form.data["article_text"]
        articles = Article.query.filter(
            Article.summary.ilike(f"%{search_query}%")
        ).all()
    else:
        search_query = False
        articles = Article.get_all_articles()

    return dict(articles=articles, search_query=search_query, feeds=Feed.get_all_feeds())
