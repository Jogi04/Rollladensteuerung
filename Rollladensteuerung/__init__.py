from flask import Flask

app = Flask(__name__)

from Rollladensteuerung import routes
