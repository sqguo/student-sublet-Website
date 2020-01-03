import os
from urllib import parse


class Config(object):
    APP_SECRET = os.urandom(24)
    BASE_URL = os.environ['BASE_URL']
    OAUTH_API_BASE = os.environ['OAUTH_API_BASE']
    OAUTH_CLIENT_ID = os.environ['OAUTH_CLIENT_ID']
    OAUTH_CLIENT_SECRET = os.environ['OAUTH_CLIENT_SECRET']

    AZ_SQLDB_NAME = os.environ['AZ_SQLDB_NAME']
    AZ_SQLDB_UID = os.environ['AZ_SQLDB_UID']
    AZ_SQLDB_PWD = os.environ['AZ_SQLDB_PWD']

    AZ_SQLDB_PARAM = parse.quote_plus('Driver={ODBC Driver 17 for SQL Server};'
                                      + 'Server=tcp:' + AZ_SQLDB_NAME
                                      + '.database.windows.net,1433;'
                                      + 'Database=' + AZ_SQLDB_NAME
                                      + ';Uid=' + AZ_SQLDB_UID
                                      + ';Pwd=' + AZ_SQLDB_PWD
                                      + ';Encrypt=yes;'
                                      + 'TrustServerCertificate=no;'
                                      + 'Connection Timeout=30;')

    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % AZ_SQLDB_PARAM
    SQLALCHEMY_TRACK_MODIFICATIONS = False
