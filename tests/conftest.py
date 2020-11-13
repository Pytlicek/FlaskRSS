import pytest
from app import app, db
from app.models import User
from flask_bcrypt import generate_password_hash
from datetime import datetime

app.config["FLASK_ENV"] = "TEST"
app.config["WTF_CSRF_ENABLED"] = False
app.config["WTF_CSRF_SECRET_KEY"] = "S3cR3t"

db.drop_all()
db.create_all()

user_1 = User()
user_1.id = 1
user_1.username = "admin"
user_1.password = generate_password_hash("admin").decode("utf8")
db.session.add(user_1)
db.session.commit()


@pytest.fixture(scope="session", autouse=True)
def client():
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client
