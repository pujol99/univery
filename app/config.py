import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = '33f34707eab125483d3dc627c4b170c8'
    SQLALCHEMY_TRACK_NOTIFICATIONS = True
    SECRET_KEY = 'sqlite:///site.db'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)