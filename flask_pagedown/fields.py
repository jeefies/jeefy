from wtforms.fields import TextAreaField
from .widgets import PageDown


class PageDownField(TextAreaField):
    widget = PageDown()

    def __init__(self, *args, rows = None, **kwargs):
        super().__init__(*args, **kwargs)
        if rows:self.widget.rows = rows
