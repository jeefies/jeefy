from flask import Blueprint

video = Blueprint('2021_video', __name__)

from ..imps import *

@video.route('/')
def index():
    return render_template('2021video/index.html')
