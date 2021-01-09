from .bp import birth
from ..imps import *

@birth.route('/')
def index():
    return render_template('birth/index.html')
