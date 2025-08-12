from extension import db 
from flask import current_app
# from itsdangerous import URLSafeTimedSerializer as Serializer # type: ignore
from itsdangerous import URLSafeTimedSerializer as Serializer 
from flask_login import UserMixin # type: ignore
from sqlalchemy.sql import func # type: ignore
from datetime import datetime


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    typeof = db.Column(db.String(100), nullable=False)
    input_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='queued')
    time_needed = db.Column(db.DateTime)
    error_happened = db.Column(db.String(3), default='no')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('assessor.a_id'))
