import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "SecretPass"

    if os.environ.get("FLASK_ENV") == "TEST":
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "./tests/test.db")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
