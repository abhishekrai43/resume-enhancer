# app/routes.py
import os
from flask import Blueprint, request, jsonify
from app.services.pdf_processor import PDFProcessor
from app.services.docx_processor import DOCXProcessor
from app.services.ai_enhancer import AIEnhancer
from app.utils.file_validator import allowed_file

routes = Blueprint("routes", __name__)

# Supported processors
PROCESSORS = {
    "pdf": PDFProcessor(),
    "docx": DOCXProcessor(),
}

# AI Enhancer setup
AI_API_KEY = "your_openai_api_key"  # Replace with your key
ai_enhancer = AIEnhancer(api_key=AI_API_KEY)

@routes.route("/upload", methods=["POST"])
def upload_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    file_extension = file.filename.rsplit(".", 1)[1].lower()
    processor = PROCESSORS.get(file_extension)

    if not processor:
        return jsonify({"error": "No processor available for this file type"}), 400

    # Save the uploaded file
    upload_path = os.path.join("uploads", file.filename)
    file.save(upload_path)

    try:
        # Extract text from the file
        resume_text = processor.extract_text(upload_path)

        # Enhance the resume with AI
        enhanced_resume = ai_enhancer.enhance_resume(resume_text)

        # Return the enhanced resume
        return jsonify({"enhanced_resume": enhanced_resume}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up uploaded file
        if os.path.exists(upload_path):
            os.remove(upload_path)
