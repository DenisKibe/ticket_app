import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"

    NYSQL_SETTINGS={'db':'ticket_db'}