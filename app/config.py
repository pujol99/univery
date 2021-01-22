import os,json
from datetime import timedelta

#with open('/etc/config.json') as config_file:
	#config = json.load(config_file)

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'#config.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = '33f34707eab125483d3dc627c4b170c8'#config.get('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=45)
