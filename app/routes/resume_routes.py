import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.resume_model import Resume
from app.models.user_model import User
from app import db
import base64

resume_routes = Blueprint('resume_routes', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Get User Resumes
@resume_routes.route('/list', methods=['GET'])
@jwt_required()
def list_resumes():
    user_id = get_jwt_identity()
    resumes = Resume.query.filter_by(user_id=user_id).all()
    resume_list = [{"id": r.id, "title": r.title, "file_url": r.file_url} for r in resumes]

    return jsonify(resume_list)



@resume_routes.route("/user-profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    identity = get_jwt_identity()
    print(f"Identity Type: {type(identity)}, Value: {identity}")

    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)

    if user:
        return jsonify({"name": user.name, "profile_pic": user.profile_pic})
    else:
        return jsonify({"error": "User not found"}), 404


# ✅ Upload Resume with Binary File Storage
@resume_routes.route("/upload", methods=["POST"])
@jwt_required()
def upload_resume():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    file = request.files.get("resume_file")
    title = request.form.get("title")

    if not file or not title:
        return jsonify({"error": "Both file and title are required"}), 400

    file_data = file.read()

    new_resume = Resume(user_id=user.id, title=title, file_data=file_data)
    db.session.add(new_resume)
    db.session.commit()

    return jsonify({"message": "Resume uploaded successfully!"})


@resume_routes.route("/user-resumes", methods=["GET"])
@jwt_required()
def get_user_resumes():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    resumes = [{"id": r.id, "title": r.title} for r in user.resumes]

    return jsonify(resumes)


# ✅ Upload Profile Picture (Directly into DB as Binary Data)
@resume_routes.route("/upload-profile-pic", methods=["POST"])
@jwt_required()
def upload_profile_pic():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    file = request.files.get("profile_pic")
    if not file:
        return jsonify({"error": "Profile picture is required"}), 400

    file_data = file.read()
    user.profile_pic = file_data  # Save binary data in DB
    db.session.commit()

    profile_pic_base64 = base64.b64encode(file_data).decode('utf-8')

    return jsonify({"message": "Profile picture uploaded successfully", "profile_pic": profile_pic_base64})

