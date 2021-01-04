from .bp import js
from ..imps import *

@js.route('/')
def index():
    return render_template('js/index.html', url = url_for('.data'))

@js.route('/data')
def data():
    data = {'key': 'val', "method": req.method}
    return jsonify(data)
