from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp

class RegistForm(FlaskForm):
    name = StringField("Name:", validators = [DataRequired()])
    email = StringField("Email:", validators = [Email(), DataRequired()])
    pwd = PasswordField("Password:", validators = [Length(8, 20, message = "Length must between 8 and 20"),
        EqualTo('vpwd', message = "Two password must macth")])
    vpwd = PasswordField("Confirm Password:", validators = [])
    submit = SubmitField("Regist")

class LoginForm(FlaskForm):
    name = StringField("Name or Email:", validators = [DataRequired()])
    pwd = PasswordField("Password:", validators = [DataRequired()])
    rem = BooleanField("Keep logged in")
    submit = SubmitField("Login")
