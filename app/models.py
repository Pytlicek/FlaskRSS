from flask_login import UserMixin
from flask_bcrypt import check_password_hash
from datetime import datetime
from sqlalchemy import desc
from app import db
import feedparser
import requests


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    def verify_password(self, password):
        """
        Verify password during login
        Returns True or False
        """
        return check_password_hash(self.password, password)


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)

    def __repr__(self):
        return repr([self.id, self.name, self.url])

    @staticmethod
    def add_feed(name, url):
        """
        Add feed to DB.
        Field feed.id is automatically added by DB engine
        """
        new_feed = Feed()
        new_feed.name = name
        new_feed.url = url
        try:
            db.session.add(new_feed)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @staticmethod
    def edit_feed(feed_id, feed_name, feed_url):
        """
        Edit selected feed based on feed_id
        Change only feed.name and feed.url
        """
        feed = Feed.query.filter_by(id=feed_id).first()
        feed.name = feed_name
        feed.url = feed_url
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @staticmethod
    def delete_feed(feed_id):
        """
        Delete selected feed with all related articles
        """
        feeds = Feed.get_feed_by_id(feed_id)
        if feeds is None or feeds == []:
            return False
        db.session.delete(feeds[0])
        db.session.commit()
        Article.delete_articles_by_feed_id(feed_id)
        return True

    @staticmethod
    def get_all_feeds():
        """
        Returns all feeds as array
        """
        return Feed.query.all()

    @staticmethod
    def get_feed_by_id(feed_id):
        """
        Returns selected feed as array
        """
        return Feed.query.filter_by(id=feed_id).all()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    title = db.Column(db.Text)
    summary = db.Column(db.Text)
    published = db.Column(db.DateTime, default=datetime.utcnow())
    feed_id = db.Column(
        db.Integer,
        db.ForeignKey("feed.id", onupdate="CASCADE", ondelete="CASCADE"),
    )

    def __repr__(self):
        return repr([self.id, self.url, self.title])

    @property
    def feed_name(self):
        """
        Add feed name as property for Article object
        """
        feed = Feed.query.filter_by(id=self.feed_id).first()
        return feed.name

    @staticmethod
    def get_all_articles():
        """
        Returns all articles in all feeds as array
        """
        return Article.query.all()

    @staticmethod
    def get_last_articles():
        """
        Returns last 300 articles in all feeds as array
        """
        return Article.query.order_by(desc(Article.id)).limit(300).all()

    @staticmethod
    def get_articles_by_feed_id(feed_id):
        """
        Returns all articles in selected feed as array
        """
        return Article.query.filter_by(feed_id=feed_id).order_by(desc(Article.id)).limit(300).all()

    @staticmethod
    def get_all_articles_by_feed_id(feed_id):
        """
        Returns all articles in selected feed as array
        """
        return Article.query.filter_by(feed_id=feed_id).all()

    @staticmethod
    def get_article_by_url(url):
        """
        Returns selected article
        """
        return Article.query.filter_by(url=url).first()

    @staticmethod
    def delete_articles_by_feed_id(feed_id):
        """
        Delete all articles in selected feed
        """
        Article.query.filter_by(feed_id=feed_id).delete()
        db.session.commit()
        return True

    @staticmethod
    def cleanup():
        """
        Cleanup DB
        """
        for feed in Feed.get_all_feeds():
            all_articles = Article.get_all_articles_by_feed_id(feed.id)
            print(f"{feed.id} / {feed.name} / articles:", len(all_articles))

            del_articles = Article.query.filter_by(feed_id=feed.id).order_by(
                desc(Article.id)).offset(300)
            for article in del_articles:
                Article.query.filter_by(id=article.id).delete()
            db.session.commit()
        return True


def download_articles(feed_url, feed_id):
    """
    Download articles for selected feed
    Takes feed url and tries to parse RSS feed
    Ensure valid RSS feed by searching for title
    Articles in the parsed feed are mapped to Article object and saved to DB
    Articles that are in DB (based on URL) are skipped and not added
    Returns list of newly added articles
    """

    feed_data = requests.get(feed_url)
    NewsFeed = feedparser.parse(feed_data.text)
    feed_problem = "title" not in NewsFeed.feed
    if feed_problem:
        return "Rate limit or invalid RSS: " + str(feed_url) + str("\n")

    articles_added = []
    for entry in NewsFeed.entries:
        if Article.get_article_by_url(entry.link) is None:
            article = Article()
            article.url = entry.link
            article.title = entry.title
            article.summary = str(entry.summary)
            article.published = datetime.now()
            article.feed_id = feed_id
            try:
                db.session.add(article)
                db.session.commit()
                articles_added.append(article.url)
            except:
                db.session.rollback()
    return (
        ["Articles downloaded for: {}\n".format(feed_url)]
        if len(articles_added) < 1
        else articles_added
    )
