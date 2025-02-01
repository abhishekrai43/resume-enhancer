import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "xyz3452@")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    JWT_SECRET_KEY = "TEST@123"

