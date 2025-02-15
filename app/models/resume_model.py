from app import db
from datetime import datetime

class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)  # 🆕 Add This!
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
