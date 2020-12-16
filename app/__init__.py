from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_sijax, os

path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

app=Flask(__name__)
app.config.from_object(Config)

db=SQLAlchemy(app)
migrate=Migrate(app, db)
#db.init_app(app)
app.config['SIJAX_STATIC_PATH']=path
app.config['SIJAX_JSON_URI']='static/js/sijax/json2.js'
flask_sijax.Sijax(app)

from app import routes

from app.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)
from app.api.views import api_blueprint
app.register_blueprint(api_blueprint)
