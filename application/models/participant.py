from application import db 
from flask import current_app
# from itsdangerous import URLSafeTimedSerializer as Serializer # type: ignore
from itsdangerous import URLSafeTimedSerializer as Serializer 
from flask_login import UserMixin # type: ignore
from sqlalchemy.sql import func # type: ignore
from datetime import datetime


class Participants(db.Model , UserMixin):
    p_id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(50))  # New
    p_group = db.Column(db.String(25))
    p_leader = db.Column(db.String(25))
    p_title = db.Column(db.String(50))

class Assessor(db.Model, UserMixin):
    # a_id = db.Column(db.Integer, primary_key=True)
    a_id = db.Column(db.Integer, primary_key=True)
    # a_uniq_id = db.Column(db.String(20))
    a_email = db.Column(db.String(40), unique=True)
    a_password = db.Column(db.String(40))
    a_name = db.Column(db.String(40))  # New
    a_gender = db.Column(db.String(10))  # New
    a_username = db.Column(db.String(40), unique=True)  # New
    notes = db.relationship('Note')

    def get_id(self):
        """Return the a_id attribute of the Assessor as a unicode string."""
        return str(self.a_id)
    def get_reset_token(self,expires_sec = 180):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)   
        return s.dumps({'user_id':self.a_id},salt='email-reset').encode('utf-8')
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'], salt='email-reset')
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Assessor.query.get(user_id)

