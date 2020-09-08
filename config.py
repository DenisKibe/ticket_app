import os

class Config(object):
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://{user}:{pass}@nyuki.postgres.database.azure.com:5432/ticketApp?sslmode=require'.format(user='DenisKibe@nyuki',pass='#Wanyugik18')
    CSRF_ENABLED=True
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    
class ProductionConfig(Config):
    DEBUG = False
    
class StagigConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True