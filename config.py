import os

class Config(object):
    APP_SECRET = os.urandom(24)
    BASE_URL = os.environ['BASE_URL']
    OAUTH_API_BASE = os.environ['OAUTH_API_BASE']
    OAUTH_CLIENT_ID = os.environ['OAUTH_CLIENT_ID']
    OAUTH_CLIENT_SECRET = os.environ['OAUTH_CLIENT_SECRET']
