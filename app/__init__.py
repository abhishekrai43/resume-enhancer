from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config
from flask_cors import CORS
# Initialize extensions
db = SQLAlchemy() 
jwt = JWTManager()  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    # Register Blueprints
    from app.routes.auth_routes import auth_routes
    from app.routes.resume_routes import resume_routes
    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(resume_routes, url_prefix="/resume")

    return app

