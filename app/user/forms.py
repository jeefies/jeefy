from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, \
        TextAreaField, DateTimeField, DateField, RadioField, \
        SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from flask_pagedown.fields import PageDownField

class RegistForm(FlaskForm):
    name = StringField("Name:", validators = [DataRequired(), Length(0, 20, message="the given name is too long, at most 20 characters")])
    email = StringField("Email:", validators = [Email(), DataRequired(), Length(1, 20, message="email addr is too long")])
    role = SelectField("Role", [DataRequired()], choices = (('Student', 'Student'),
        ('Teacher', 'Teacher'), ('Worker', 'Worker'), ('Other', 'Other'),
        ('Visitor', 'Visitor'),), default="Other")
    pwd = PasswordField("Password:", validators = [Length(8, 20,
            message = "Length must between 8 and 20"),
        EqualTo('vpwd', message = "Two password must macth")])
    vpwd = PasswordField("Confirm Password:", validators = [])
    submit = SubmitField("Regist")

class LoginForm(FlaskForm):
    name = StringField("Name or Email:", validators = [DataRequired()])
    pwd = PasswordField("Password:", validators = [DataRequired()])
    rem = BooleanField("Keep logged in")
    submit = SubmitField("Login")

class DetailForm(FlaskForm):
    birth = DateField("Birthday (YYYY-MM-DD)")
    sex = RadioField("Gender", [DataRequired()], choices = (("Male", "Male"),
        ("Female", "Female")), default="Male")
    desc = TextAreaField("Description to yourself(markdown type)", validators = [DataRequired()])
    submit = SubmitField("Verify")
