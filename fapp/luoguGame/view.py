"""
views:
    /generate: Generate an qrcode!
"""

import time
import base64
from io import BytesIO

from .bp import luoguGame
from ..imps import *

import qrcode

@luoguGame.route('/generate')
def generate():
    ns = time.time_ns()
    ct = str(bin(ns)[2:]).encode()
    
    print(f"{ns} {base64.b64encode(ct)}")
    
    img = qrcode.make(base64.b64encode(ct))

    bio = BytesIO()
    img.save(bio, "jpeg")

    bio.seek(0)
    return send_file(bio, "image/jpeg", True, "qrcode.jpg")
