import os
from settings import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))
html_dir = os.path.join(basedir, '..', 'html')
app = Flask(__name__,
            template_folder=html_dir,
            static_folder=html_dir)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from yacut import models
from . import views
