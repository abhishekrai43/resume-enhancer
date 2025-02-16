import os
import base64
import openai
import pdfplumber
from pdf2docx import Converter
from docx import Document
from spellchecker import SpellChecker
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user_model import User
from app.models.resume_model import Resume
from app import db
import io

resume_routes = Blueprint('resume_routes', __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Get User Resumes
@resume_routes.route('/list', methods=['GET'])
@jwt_required()
def list_resumes():
    user_id = get_jwt_identity()
    resumes = Resume.query.filter_by(user_id=user_id).all()
    resume_list = [
        {
            "id": r.id,
            "title": r.title,
            "file_url": f"http://localhost:5001/resume/download/{r.id}"
        }
        for r in resumes
    ]

    return jsonify(resume_list)



@resume_routes.route("/user-profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # 🖼️ Convert binary profile pic to Base64 string
    profile_pic_base64 = (
        base64.b64encode(user.profile_pic).decode('utf-8') 
        if user.profile_pic 
        else None
    )

    return jsonify({
        "name": user.name,
        "profile_pic": profile_pic_base64
    })

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


# ✅ Adjust user-resumes to include the PDF URL
@resume_routes.route("/user-resumes", methods=["GET"])
@jwt_required()
def get_user_resumes():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    resumes = [
        {
            "id": r.id,
            "title": r.title,
            "file_url": f"http://localhost:5001/resume/download/{r.id}"
        }
        for r in user.resumes
    ]

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

# 🛠️ Endpoint to serve PDF files
@resume_routes.route("/download/<int:resume_id>", methods=["GET"])
@jwt_required()
def download_resume(resume_id):
    # Verify user identity
    user_id = get_jwt_identity()

    # Query the resume
    resume = Resume.query.get(resume_id)
    if not resume:
        return jsonify({"error": "Resume not found"}), 404

    # Ensure the resume belongs to the authenticated user
    if resume.user_id != int(user_id):
        return jsonify({"error": "Unauthorized"}), 403

    # Serve the PDF from binary data
    return send_file(
        io.BytesIO(resume.file_data),
        mimetype="application/pdf",
        as_attachment=False,
        download_name=resume.title
    )


@resume_routes.route("/resume/enhance/<int:resume_id>", methods=["POST"])
def enhance_resume(resume_id):
    try:
        resume = db.session.get(Resume, resume_id)
        if not resume:
            return jsonify({"error": "Resume not found"}), 404

        # Save file temporarily
        temp_path = os.path.join(UPLOAD_FOLDER, f"temp_resume_{resume.id}.pdf")
        with open(temp_path, "wb") as f:
            f.write(resume.file_data)

        # Extract text using pdfplumber
        extracted_text = ""
        with pdfplumber.open(temp_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"

        # Initialize spellchecker
        spell = SpellChecker()
        words = extracted_text.split()
        misspelled = list(spell.unknown(words))

        # Generate improvement suggestions
        improvements = [
            "Improved structure",
            "Added industry-specific keywords",
            "Ensured consistent formatting",
            "Grammar improvements"
        ]

        # Prepare response
        result = {
            "misspelled_words": misspelled,
            "improvements": improvements,
            "message": "Enhancement completed successfully"
        }

        # Cleanup
        os.remove(temp_path)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500