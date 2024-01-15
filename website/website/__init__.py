from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from os import path
from flask_login import LoginManager
from sqlalchemy import *
import pymysql

# RDS Connection
pymysql.install_as_MySQLdb()
rdsConnection = create_engine("mysql+mysqldb://admin:passwordRDS@nemesisrds.cjmjlsxabz75.us-east-1.rds.amazonaws.com/")

# creates the database instance (SQLAlchemy)
db = SQLAlchemy()
DB_NAME = "users"

def create_app():
    app = Flask(__name__)  # create app instance
    app.config['SECRET_KEY'] = 'test'  # connects app file to the database
    # used to secure the session cookie
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # SQLite DB
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://admin:passwordRDS@nemesisrds.cjmjlsxabz75.us-east-1.rds.amazonaws.com/users'  # MySQL DB
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import user_info

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return user_info.query.get(int(id))

    return app

# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
