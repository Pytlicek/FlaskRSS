import pytest
from app import app, db
from app.models import User, Feed
from flask_bcrypt import generate_password_hash
from datetime import datetime

app.config["FLASK_ENV"] = "TEST"
app.config["WTF_CSRF_ENABLED"] = False
app.config["WTF_CSRF_SECRET_KEY"] = "S3cR3t"

db.drop_all()
db.create_all()

user_1 = User()
user_1.id = 0
user_1.username = "admin"
user_1.password = generate_password_hash("admin").decode("utf8")
user_1.blocked_words = "NON_EXISTING_WORD"
db.session.add(user_1)
db.session.commit()

feed_0 = Feed()
feed_0.id = 0
feed_0.name = "Trash"
feed_0.url = "http://trash"
feed_0.show_in_feed = 0
feed_0.updated = datetime.now()
db.session.add(feed_0)
db.session.commit()


@pytest.fixture(scope="session", autouse=True)
def client():
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client
