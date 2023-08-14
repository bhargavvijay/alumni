from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_session import Session
from flask_login import LoginManager
from flask_migrate import Migrate
db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    db.init_app(app)
    migrate = Migrate(app, db)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Company_User,Job

    with app.app_context():
        all_users = User.query.all()

        # Print the contents of the 'User' table
        for user in all_users:
            print("User Email: {}, First Name: {},password: {},login_first: {},age:{}".format(user.email, user.first_name,user.password,user.login_first,user.age))

        # Retrieve all company users from the 'Company_User' table
        all_users = Company_User.query.all()

        # Print the contents of the 'Company_User' table
        print("\n\n\n\n\n\n")
        for user in all_users:
            print("User Email: {}, First Name: {},password: {}".format(user.email, user.company_name, user.password))

        all_jobs = Job.query.all()

        for jobs in all_jobs:
            print(jobs.qualifications_required,jobs.title)

        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.companylogin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_company_user(id):
        return Company_User.query.get(int(id))

    login_manager = LoginManager()
    login_manager.login_view = 'auth.alumnilogin'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

