# application/app.py
import os
from flask import Flask
from extension import db, mail, login_manager  # <-- local, top-level imports
# from extension
app = Flask(__name__)
app.config['SECRET_KEY'] = 'createapp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@database-1.cdgyssu446lk.us-east-1.rds.amazonaws.com:5432/db_init'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Mail config (move to env vars in real use)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'try.nachiket@gmail.com'
app.config['MAIL_PASSWORD'] = 'ngmm cumk vjnv vopl'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# init extensions
db.init_app(app)
mail.init_app(app)
login_manager.login_view = 'admin.login'
login_manager.init_app(app)

# import AFTER initializing extensions to avoid circulars
from routes.llmwork import LLM
from models import Assessor

app.register_blueprint(LLM, url_prefix='/')

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Assessor.query.get(int(user_id))

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "1") == "1"
    )
