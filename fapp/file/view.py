"""
File Upload, save and download subsystem.
prefix: /files
"""
from .bp import filebp

@filebp.route('/')
def index():
    return "FILE"
