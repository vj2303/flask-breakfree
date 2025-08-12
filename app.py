# from flask import Flask
# from models import db
# from routes import main_blueprint

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///breakfreeai.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)

# app.register_blueprint(main_blueprint)

# if __name__ == '__main__':
#     app.run(debug=True) 

# app.py
import os
from application import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "1") == "1"
    )
