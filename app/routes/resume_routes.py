from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.resume_model import Resume
from app import db
import os
from datetime import datetime

resume_routes = Blueprint("resume_routes", __name__)

@resume_routes.route("/upload", methods=["POST"])
@jwt_required()
def upload_resume():
    user_id = get_jwt_identity()
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Use app's config for the upload folder
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    filename = file.filename
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    new_resume = Resume(
        user_id=user_id,
        original_filename=filename,
        upload_time=datetime.utcnow(),
    )
    db.session.add(new_resume)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully", "resume_id": new_resume.id}), 201
