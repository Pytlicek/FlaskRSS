from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


class AddFeedForm(FlaskForm):
    name = StringField("Name (Tag)", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired()])
    show_in_feed = BooleanField("Include in feed", default=True)
    submit = SubmitField("Add Feed")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class SearchForm(FlaskForm):
    article_text = StringField(
        "Search", validators=[DataRequired(), Length(max=60)]
    )
