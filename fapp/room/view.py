"""
Room chat blueprint
prefix : /chat
"""

from .bp import room

@room.route('/')
def index():
    return "ROOM"
