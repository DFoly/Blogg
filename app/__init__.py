# this is the app package constructor

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name): # development, production, testing??
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    main.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # NB put at end of function to avoid circular dependencies
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
