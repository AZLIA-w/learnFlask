from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"




def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcdefghijklmnopqrsj'
    # database的地址
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # 初始化database
    db.init_app(app)
    from .models import User,Note
    with app.app_context():
        creat_database()

    login_manager = LoginManager()
    # if not login and then gose to lgin pages
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    #tell flask how we load a user,we  load this id
    #automantly search the primaryKey
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .viewes import views
    from .auth import auth

    app.register_blueprint(views,url_prefix = '/')
    app.register_blueprint(auth,url_prefix = '/')



  

    return app

# check database exists or not
def creat_database():
    if not path.exists('website/' + DB_NAME):
        # 传入的app与上方creatApp一致 指向的地址也一致  app.config['SQLALCHEMY_DATABASE_URL'] = f'sqlite:///{DB_NAME}'
        db.create_all()     
        print('Created Datebase!')