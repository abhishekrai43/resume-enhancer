from app import db

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    original_filename = db.Column(db.String(120), nullable=False)
    enhanced_filename = db.Column(db.String(120), nullable=True)
    upload_time = db.Column(db.DateTime, nullable=False)
