from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class FileForm(FlaskForm):
    file = FileField("Please Choose a file you'd like to upload",
            validators = [DataRequired(message = 'There no FILE input!')])
    puc = BooleanField("Public")
    submit = SubmitField('upload')

    @classmethod
    def iupdate(cls):
        cls.file.data = None 
