import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_NOTIFICATIONS = True
    SECRET_KEY = '33f34707eab125483d3dc627c4b170c8'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)