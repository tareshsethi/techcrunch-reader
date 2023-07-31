from flask import Flask

from app.env import *

app = Flask(__name__)
logger = app.logger
from app import routes

app.config['DEBUG'] = DEBUG
