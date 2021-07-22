from functools import lru_cache
from .bp import birth
from ..imps import *

@birth.route('/')
@lru_cache()
def index():
    return render_template('birth/index.html')
