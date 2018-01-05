from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    # type: (object) -> object
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # print(app.config['SECRET_KEY'])
    # print(app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'])
    # print(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
    # print(app.config['MAIL_SERVER'])
    # print(app.config['MAIL_PORT'])
    # print(app.config['MAIL_USE_TLS'])
    # print(app.config['MAIL_USERNAME'])
    # print(app.config['MAIL_PASSWORD'])
    # print(app.config['FLASKY_MAIL_SUBJECT_PREFIX'])
    # print(app.config['FLASKY_MAIL_SENDER'])
    # print(app.config['FLASKY_ADMIN'])

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
