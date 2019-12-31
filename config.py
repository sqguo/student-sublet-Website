import os

class Config(object):
    APP_SECRET = os.urandom(24)
    BASE_URL = os.environ.get['BASE_URL']
    OAUTH_API_BASE = os.environ.get['OAUTH_API_BASE']
    OAUTH_CLIENT_ID = os.environ.get['OAUTH_CLIENT_ID']
    OAUTH_CLIENT_SECRET = os.environ.get['OAUTH_CLIENT_SECRET']
