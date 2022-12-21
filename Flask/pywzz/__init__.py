from flask import Flask #basic
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__) #기본
    app.config.from_object(config) #sql

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    # 블루프린트
    from .views import main_views,auth_views, check_views,question_views,answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(check_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)

    return app