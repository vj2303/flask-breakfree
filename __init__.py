from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'createapp'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@database-1.cdgyssu446lk.us-east-1.rds.amazonaws.com:5432/db_init'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'try.nachiket@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ngmm cumk vjnv vopl'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    db.init_app(app)
    mail.init_app(app)

    # ✅ Only keep the blueprint you need
    from .routes.llmwork import LLM
    app.register_blueprint(LLM, url_prefix='/')

    # ✅ Import models so Flask-Migrate / db.create_all sees them
    # from .models import (
    #     Report, Note, Participants,
    #     CaseStudyAnalysis, GroupDiscussion
    # )

    # Ensure the database tables exist
    with app.app_context():
        db.create_all()

    # Flask-Login config
    login_manager = LoginManager()
    login_manager.login_view = 'admin.login'
    login_manager.init_app(app)

    # This assumes you have an Assessor model in models
    from .models import Assessor

    @login_manager.user_loader
    def load_user(id):
        return Assessor.query.get(int(id))

    return app
