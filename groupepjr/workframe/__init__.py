from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os import path
from pyngrok import conf, ngrok
import config

db = SQLAlchemy()
DB_NAME = 'workframe.db'
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .view import main_views
    app.register_blueprint(main_views.bp)

    return app
