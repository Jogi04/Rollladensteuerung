from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shutters.db'
db = SQLAlchemy(app)

from Rollladensteuerung import routes