from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class FileForm(FlaskForm):
    file = FileField("Please Choose a file you'd like to upload",
            validators = [DataRequired(message = 'There no FILE input!')])
    submit = SubmitField('upload')

    @classmethod
    def iupdate(cls):
        cls.file = FileField("Please Choose a file you'd like to upload",
            validators = [DataRequired(message = 'There no FILE input!')])
        cls.submit = SubmitField('upload')
