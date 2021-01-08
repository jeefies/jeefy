from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, \
        TextAreaField, DateTimeField, DateField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from flask_pagedown.fields import PageDownField

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

class DetailForm(FlaskForm):
    birth = DateField("Birthday")
    sex = RadioField("Gender", [DataRequired()], choices = (("Male", "Male"), ("Female", "Female")), default="Male")
    desc = PageDownField("Description to yourself(markdown type)", validators = [DataRequired()], rows= 5)
    submit = SubmitField("Verify")
