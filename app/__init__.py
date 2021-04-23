from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db: SQLAlchemy = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "thisismysecretkey!!"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
    db.init_app(app)
    db.app = app

    login_manager = LoginManager()
    login_manager.login_view = '/login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from .auth import auth
    app.register_blueprint(auth)

    from .management import manage
    app.register_blueprint(manage)

    return app
