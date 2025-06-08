from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user_model import User
from app import db
from werkzeug.security import check_password_hash

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")  #  Get Name from Request
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    existing_user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
    
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(name=name, email=email)  #  Save Name
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=str(new_user.id))
    return jsonify({"message": "User registered successfully", "access_token": access_token}), 201


@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "access_token": access_token,
            "message": f"Welcome back, {user.name}!"
        }), 200

    return jsonify({"error": "Invalid username or password"}), 401

@auth_routes.route("/upload_profile_pic", methods=["POST"])
def upload_profile_pic():
    user_id = request.form.get("user_id")
    image = request.files.get("profile_pic")

    if not user_id or not image:
        return jsonify({"error": "User ID and profile picture are required"}), 400

    #  Read the image data as bytes
    image_data = image.read()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    #  Save image data in the database
    user.profile_pic = image_data
    db.session.commit()

    return jsonify({"message": "Profile picture uploaded successfully"}), 200


@auth_routes.route("/get_profile_pic/<int:user_id>", methods=["GET"])
def get_profile_pic(user_id):
    user = User.query.get(user_id)
    if not user or not user.profile_pic:
        return jsonify({"error": "No profile picture found"}), 404

    #  Serve the image data as a response
    from flask import Response
    return Response(user.profile_pic, mimetype='image/jpeg')