from app import app, db
from app.models import User, Feed

app.config["DEBUG"] = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

print("\nCreating DB Tables")
try:
    db.drop_all()
    db.create_all()
    print("Tables Created")
except Exception as e:
    print(e)
    print("Problem creating tables. Check DB connection parameters")

try:
    user = User()
    user.id = 0
    user.username = "admin"
    user.password = (
        "$2b$12$K6WtZoPwFi8yLmu20za5E.mJiW15vYmHDYJ1jLxR9IytJrSV/x32y"  # admin
    )
    db.session.add(user)
    db.session.commit()
    print("User created admin/admin")
except Exception as e:
    print(e)
    print("Problem in User creation")
