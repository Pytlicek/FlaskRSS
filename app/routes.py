from flask import render_template, url_for, redirect, flash
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
)
from app import app
from app.forms import LoginForm
from app.models import User, Feed, Article, download_articles
from app.forms import AddFeedForm

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
        login_user(user)
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return render_template("dashboard_index.html")


@app.route("/feeds", methods=["GET", "POST"])
@login_required
def feeds_index():
    form = AddFeedForm()
    if form.validate_on_submit():
        Feed.add_feed(form.data["name"], form.data["url"])
        flash("Feed has been added", "success")
    feeds = Feed.get_all_feeds()
    return render_template("feeds_index.html", feeds=feeds, form=form)


@app.route("/feeds/<feed_id>/delete", methods=["GET"])
@login_required
def feeds_delete(feed_id):
    if Feed.delete_feed(feed_id) is True:
        flash("Feed has been deleted", "success")
    return redirect(url_for("feeds_index"))


@app.route("/feeds/download/", defaults={"feed_id": None}, methods=["GET"])
@app.route("/feeds/download/<feed_id>")
@login_required
def feeds_download(feed_id):
    if feed_id is None:
        feeds = Feed.get_all_feeds()
    else:
        feeds = Feed.get_feed_by_id(feed_id)

    articles_list = []
    for feed in feeds:
        articles = download_articles(feed.url, feed.id)
        articles_list += articles
    return render_template("feeds_download.html", articles_list=articles_list)


@app.route("/feeds/articles", defaults={"feed_id": None}, methods=["GET"])
@app.route("/feeds/<feed_id>/articles/")
@login_required
def feeds_articles(feed_id):
    if feed_id is None:
        articles = Article.get_all_articles()
    else:
        articles = Article.get_articles_by_feed_id(feed_id)

    feeds = Feed.get_all_feeds()
    return render_template(
        "articles_index.html", articles=articles, feeds=feeds
    )
