from flask_login import UserMixin, current_user
from flask_bcrypt import check_password_hash
from datetime import datetime
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
    )

    def __repr__(self):
        return repr([self.id, self.name, self.url])

    @staticmethod
    def add_feed(name, url):
        new_feed = Feed()
        new_feed.name = name
        new_feed.url = url
        new_feed.user_id = current_user.id
        try:
            db.session.add(new_feed)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @staticmethod
    def delete_feed(feed_id):
        feeds = Feed.get_feed_by_id(feed_id)
        if feeds is None or feeds == []:
            return False
        db.session.delete(feeds[0])
        db.session.commit()
        Article.delete_articles_by_feed_id(feed_id)
        return True

    @staticmethod
    def get_all_feeds():
        return Feed.query.filter_by(user_id=current_user.id).all()

    @staticmethod
    def get_feed_by_id(feed_id):
        return Feed.query.filter_by(user_id=current_user.id, id=feed_id).all()


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
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
    )

    def __repr__(self):
        return repr([self.id, self.url, self.title])

    @property
    def feed_name(self):
        feed = Feed.query.filter_by(id=self.feed_id).first()
        return feed.name

    @staticmethod
    def get_all_articles():
        return Article.query.filter_by(user_id=current_user.id).all()

    @staticmethod
    def get_articles_by_feed_id(feed_id):
        return Article.query.filter_by(feed_id=feed_id).all()

    @staticmethod
    def get_article_by_url(url):
        return Article.query.filter_by(
            user_id=current_user.id, url=url
        ).first()

    @staticmethod
    def delete_articles_by_feed_id(feed_id):
        Article.query.filter_by(
            user_id=current_user.id, feed_id=feed_id
        ).delete()
        db.session.commit()
        return True


def download_articles(feed_url, feed_id):
    import feedparser

    NewsFeed = feedparser.parse(feed_url)
    if "title" in NewsFeed.feed is False:
        return [
            "There was an error parsing the feed. Please ensure that the feed is valid RSS"
        ]

    articles_added = []
    for entry in NewsFeed.entries:
        if Article.get_article_by_url(entry.link) is None:
            article = Article()
            article.url = entry.link
            article.title = entry.title
            article.summary = str(entry.summary)
            article.published = datetime.now()
            article.feed_id = feed_id
            article.user_id = current_user.id
            try:
                db.session.add(article)
                db.session.commit()
                # print("Article Added", article.id)
                articles_added.append(article.url)
            except:
                db.session.rollback()
        else:
            # print("Article exists", entry.link)
            pass
    return articles_added
