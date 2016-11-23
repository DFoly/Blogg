from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view =  'auth.login'


def create_app(config_name): # is it test, production or development??
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint   # import global decorators
    app.register_blueprint(main_blueprint)
    
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/auth') 
    # url_prefix all routes have prefix /auth eg /auth/login
    # full url http://localhost:5000/auth/login


    return app

