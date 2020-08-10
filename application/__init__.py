from flask import Flask
from config import Config
from flask_mysqldb import MySQL


app=Flask(__name__)
app.config.from_object(Config)

db=MySQL()
db.init_app(app)


from application import routes