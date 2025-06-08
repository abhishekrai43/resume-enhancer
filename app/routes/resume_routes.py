import os
import base64
from openai import OpenAI
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user_model import User
from app.models.resume_model import Resume
from app import db
from app.config import Config
import io
from flask_cors import cross_origin
import json
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import time  
from openai import RateLimitError, APIError  
import logging  

resume_routes = Blueprint('resume_routes', __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#  Initialize OpenAI client with debugging and disabled retries
print(f"🔍 Debug: Loading OpenAI API Key...")
Config.debug_api_key()  # Debug the API key loading
client = OpenAI(
    api_key=Config.OPENAI_API_KEY,
    max_retries=0  #  Disable OpenAI SDK retries to avoid conflicts
)
print(f" OpenAI client initialized successfully")

#  Add rate limiting helper function with better error handling
def call_openai_with_retry(messages, max_retries=3, base_delay=2):
    """Call OpenAI API with exponential backoff retry logic"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=4096
            )
            return response
        except RateLimitError as e:
            if attempt == max_retries - 1:
                logging.error(f" Max retries exceeded. OpenAI quota likely exhausted.")
                raise e
            wait_time = base_delay * (2 ** attempt)
            logging.warning(f"⚠️ Rate limit hit (attempt {attempt + 1}/{max_retries}), waiting {wait_time} seconds...")
            time.sleep(wait_time)
        except APIError as e:
            logging.error(f" OpenAI API Error: {str(e)}")
            raise e
        except Exception as e:
            logging.error(f" Unexpected error: {str(e)}")
            raise e
    
    raise Exception("Max retries exceeded")

#  Get User Resumes
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

#  Upload Resume with Binary File Storage
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


#  Adjust user-resumes to include the PDF URL
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


#  Upload Profile Picture (Directly into DB as Binary Data)
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



import logging
logging.basicConfig(level=logging.DEBUG)
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


def draw_oval_background(canvas, doc):
    width, height = doc.pagesize
    canvas.saveState()
    
    #  Lighter Shades of Blue
    canvas.setFillColorRGB(0.85, 0.92, 0.98)  # Very Light Blue
    canvas.ellipse(-width * 0.4, height * 0.05, width * 1.2, height * 0.7, fill=True, stroke=False)

    canvas.setFillColorRGB(0.7, 0.85, 0.95)  # Light Blue
    canvas.ellipse(-width * 0.3, height * 0.2, width * 1.1, height * 0.8, fill=True, stroke=False)

    canvas.restoreState()


import re  #  Import regex to detect Markdown-style headers

import random  #  Import to generate random colors
import re  #  Import regex to detect Markdown-style headers

#  Define a list of professional colors for section headers
HEADER_COLORS = [
    colors.darkblue, colors.darkgreen, colors.darkred, colors.purple,
    colors.teal, colors.orange, colors.brown
]

#  Choose a single elegant color for the candidate's name
NAME_COLOR = colors.darkblue  

import random  #  Import to generate random colors
import re  #  Import regex to detect Markdown-style headers

#  Define a list of professional colors for section headers
HEADER_COLORS = [
    colors.darkblue, colors.darkgreen, colors.darkred, colors.purple,
    colors.teal, colors.orange, colors.brown
]

#  Choose a single elegant color for the candidate's name
NAME_COLOR = colors.darkblue  

def create_enhanced_resume_pdf(file_path, text_lines):
    margin = 50  #  Define margin for better layout

    doc = SimpleDocTemplate(file_path, pagesize=letter,
                            rightMargin=margin, leftMargin=margin,
                            topMargin=margin, bottomMargin=margin)
    
    styles = getSampleStyleSheet()

    #  Improved Text Formatting
    name_style = ParagraphStyle('NameStyle', parent=styles['Title'], fontSize=24, textColor=NAME_COLOR, 
                                spaceAfter=25, alignment=1, bold=True)  #  Centered, Large, Elegant Name
    bullet_style = ParagraphStyle('BulletStyle', parent=styles['Normal'], fontSize=12, textColor=colors.black, 
                                  leftIndent=25, spaceBefore=5, leading=14, bulletIndent=10)
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=12, textColor=colors.black, leading=14)

    flowables = []
    
    #  Extract Candidate's Name from the Resume (First Line)
    candidate_name = re.sub(r"\*+", "", text_lines[0].strip()) if text_lines else "Candidate Name"

    
    #  Add Candidate Name as the Main Title
    flowables.append(Paragraph(candidate_name, name_style))
    flowables.append(Spacer(1, 12))  # Add space after name

    in_section = False  # Flag to track whether we are inside a section

    for line in text_lines[1:]:  #  Skip the first line (since it's the candidate's name)
        stripped_line = line.strip().replace("**", "").replace("*", "")

        if stripped_line == "":
            flowables.append(Spacer(1, 10))  # Add space for better readability
        elif re.match(r"^\*\*(.*?)\*\*$", stripped_line):  #  Detect Markdown Headers like **TEXT**
            section_title = re.sub(r"^\*\*(.*?)\*\*$", r"\1", stripped_line)  #  Remove `**`
            
            #  Pick a random color for the header
            header_color = random.choice(HEADER_COLORS)

            #  Define a dynamic section style with different colors
            dynamic_section_style = ParagraphStyle('DynamicSectionStyle', parent=styles['Heading2'], 
                                                   fontSize=16, textColor=header_color, bold=True, spaceAfter=10)

            flowables.append(Paragraph(section_title, dynamic_section_style))
            in_section = True  # Next lines are likely bullet points
        elif stripped_line.endswith(":"):  #  Section Titles without `**`
            #  Pick a random color for the header
            header_color = random.choice(HEADER_COLORS)

            dynamic_section_style = ParagraphStyle('DynamicSectionStyle', parent=styles['Heading2'], 
                                                   fontSize=16, textColor=header_color, bold=True, spaceAfter=10)

            flowables.append(Paragraph(stripped_line, dynamic_section_style))
            in_section = True  # Next lines are likely bullet points
        elif stripped_line.startswith("- ") or (in_section and "," in stripped_line):  #  Bullet Points or Comma Lists
            bullet_items = stripped_line.split(", ") if "," in stripped_line else [stripped_line]
            for bullet in bullet_items:
                bullet = bullet.replace("- ", "").strip()
                flowables.append(Paragraph(f"• {bullet}", bullet_style))
        else:  #  Normal Text
            flowables.append(Paragraph(stripped_line, normal_style))
            in_section = False  # Reset flag

        flowables.append(Spacer(1, 6))  # Space between entries

    #  Add Footer with Candidate Name & Date
    footer_text = f"{candidate_name} | Enhanced on {datetime.now().strftime('%Y-%m-%d')}"
    flowables.append(Spacer(1, 20))
    flowables.append(Paragraph(footer_text, styles['Italic']))

    doc.build(flowables, onFirstPage=draw_oval_background, onLaterPages=draw_oval_background)


@resume_routes.route("/enhance/<int:resume_id>", methods=["POST"])
@cross_origin(supports_credentials=True)
@jwt_required()
def enhance_resume(resume_id):
    logging.debug(f"📌 Received enhancement request for resume ID: {resume_id}")

    try:
        user_id = get_jwt_identity()
        resume = db.session.get(Resume, resume_id)

        if not resume or resume.user_id != int(user_id):
            logging.error(" Resume not found or unauthorized access.")
            return jsonify({"error": "Resume not found or unauthorized"}), 403

        #  Get User Input: Job Title
        job_title = request.json.get("job_title")
        if not job_title:
            return jsonify({"error": "Job title is required for optimization"}), 400

        #  Extract Text from PDF
        temp_pdf_path = os.path.join(UPLOAD_FOLDER, f"resume_{resume_id}.pdf")
        with open(temp_pdf_path, "wb") as f:
            f.write(resume.file_data)

        pdf_reader = PdfReader(temp_pdf_path)
        extracted_text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages).strip()

        if not extracted_text:
            return jsonify({"error": "No text extracted from the resume"}), 400

        #  AI Enhancement Prompt
        prompt = (
            f"Rewrite and optimize the following resume for the job position '{job_title}'.\n"
            "- Ensure strong action verbs and concise language.\n"
            "- Improve readability and ATS (Applicant Tracking System) compatibility.\n"
            "- Tailor the resume to emphasize skills relevant to the job role.\n"
            "- Keep personal details unchanged (Name, Email, Phone, etc.).\n\n"
            "Format the response strictly as follows:\n\n"
            
            "**Errors (With Explanations):**\n"
            "- <Error Found>: <Reason why it's incorrect>\n"
            "- <Error Found>: <Reason why it's incorrect>\n\n"

            "**Suggested Keywords:**\n"
            "- <ATS keyword 1>\n"
            "- <ATS keyword 2>\n\n"
            
            "**Improvements (With Reasons):**\n"
            "- <Suggested Improvement>: <Reason for improvement>\n"
            "- <Suggested Improvement>: <Reason for improvement>\n\n"
            
            "**Enhanced Resume:**\n"
            "<BEGIN RESUME>\n"
            "<Rewritten Resume Content>\n"
            "<END RESUME>\n\n"

            "**Resume Content:**\n"
            f"{extracted_text}"
        )

        #  Send Request to OpenAI with retry logic
        try:
            response = call_openai_with_retry([
                {"role": "system", "content": "You are a professional resume optimizer."},
                {"role": "user", "content": prompt}
            ])
        except RateLimitError:
            return jsonify({
                "error": "OpenAI API quota exceeded. Please check your billing plan at https://platform.openai.com/account/billing",
                "error_type": "quota_exceeded"
            }), 429
        except APIError as e:
            return jsonify({
                "error": f"OpenAI API error: {str(e)}",
                "error_type": "api_error"
            }), 500

        ai_response = response.choices[0].message.content.strip()
        logging.debug(f"📌 AI Response Preview: {ai_response[:100]}...")
        print("\n========== RAW AI RESPONSE ==========")
        print(ai_response)
        print("========== END RAW AI RESPONSE ==========")
        #  Extract Sections Correctly
        sections = {"errors": [], "keywords": [], "improvements": []}

        if "**Errors (With Explanations):**" in ai_response:
            parts = ai_response.split("**Errors (With Explanations):**")[1]

            if "**Suggested Keywords:**" in parts:
                sections["errors"], parts = parts.split("**Suggested Keywords:**", 1)
            if "**Improvements (With Reasons):**" in parts:
                sections["keywords"], sections["improvements"] = parts.split("**Improvements (With Reasons):**", 1)

            #  Process Errors
            sections["errors"] = [{"error": e.split(":")[0].strip(), "explanation": e.split(":")[1].strip()} 
                                  for e in sections["errors"].strip().split("\n") if ":" in e]

            #  Process Keywords
            sections["keywords"] = [i.strip("- ") for i in sections["keywords"].strip().split("\n") if i]

            #  Process Improvements
            sections["improvements"] = [{"suggestion": i.split(":")[0].strip(), "reason": i.split(":")[1].strip()}
                                        for i in sections["improvements"].strip().split("\n") if ":" in i]
        else:
            return jsonify({"error": "AI response missing required sections"}), 500

        #  Extract the AI-enhanced resume content
        if "<BEGIN RESUME>" in ai_response and "<END RESUME>" in ai_response:
            enhanced_resume_text = ai_response.split("<BEGIN RESUME>")[1].split("<END RESUME>")[0].strip()
        else:
            return jsonify({"error": "AI response is not properly formatted"}), 500

        enhanced_resume_lines = enhanced_resume_text.split("\n")

        #  Generate the Final PDF
        final_pdf_path = os.path.join(UPLOAD_FOLDER, f"enhanced_resume_{resume_id}.pdf")
        create_enhanced_resume_pdf(final_pdf_path, enhanced_resume_lines)  

        #  Store Enhanced Resume & AI Feedback in Database
        with open(final_pdf_path, "rb") as f:
            resume.enhanced_file_data = f.read()

        resume.errors = json.dumps(sections["errors"])   #  Convert list of dicts to JSON
        resume.keywords = ",".join(sections["keywords"])  #  Convert list to string
        resume.improvements = json.dumps(sections["improvements"])  #  Convert list of dicts to JSON

        db.session.commit()

        return jsonify({
            "message": "Resume enhancement complete!",
            "file_url": f"http://localhost:5001/resume/download/enhanced_resume_{resume_id}.pdf",  #  Correct filename
            "errors": json.loads(resume.errors) if resume.errors else [],
            "keywords": resume.keywords.split(",") if resume.keywords else [],
            "improvements": json.loads(resume.improvements) if resume.improvements else []
        })

    except Exception as e:
        logging.error(f" Unexpected error: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


import glob  #  Import glob to find the latest file

@resume_routes.route("/download/<string:filename>", methods=["GET"])
@jwt_required()
def download_enhanced_resume(filename):
    """Serves the correct enhanced resume file from disk."""

    user_id = get_jwt_identity()

    #  Ensure filename has .pdf extension
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    #  Ensure the file exists in uploads/
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        logging.error(f"❌ Enhanced resume file not found: {file_path}")
        return jsonify({"error": "Enhanced resume file not found"}), 404

    logging.info(f" Serving enhanced resume: {file_path}")
    return send_file(file_path, mimetype="application/pdf", as_attachment=True)


