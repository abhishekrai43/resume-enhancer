from app import db

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    #  New Fields for Enhancements
    enhanced_text = db.Column(db.Text, nullable=True)  # Stores AI-enhanced text
    misspelled_words = db.Column(db.Text, nullable=True)  # Stores misspelled words
    improvements = db.Column(db.Text, nullable=True)  # Stores list of improvements
    changes = db.Column(db.JSON, nullable=True)  # Stores "Before → After" changes as structured JSON
    enhanced_file_data = db.Column(db.LargeBinary, nullable=True)  # Stores enhanced resume PDF
    enhanced_filename = db.Column(db.String(255), nullable=True)  # Stores filename for enhanced PDF
