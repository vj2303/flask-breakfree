# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return f'<User {self.username}>' 

from .report import Report, Note
from .participant import Participants, Assessor

from .competencies import GroupDiscussion, CBI, CaseStudyAnalysis , InboxActivity,  CaseStudyPresentation ,RolePlay


__all__ = [
    "Report", "Note", "Participants",
    "CaseStudyAnalysis", "GroupDiscussion",
    "InboxActivity", "RolePlay", "CaseStudyPresentation", "CBI"  ,"Assessor"
]
