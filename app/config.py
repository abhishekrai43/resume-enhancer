import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file in the app directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "xyz3452@")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    JWT_SECRET_KEY = "TEST@123"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Debug: Print API key status (first 10 chars only for security)
    @classmethod
    def debug_api_key(cls):
        api_key = cls.OPENAI_API_KEY
        if api_key:
            print(f" OpenAI API Key loaded: {api_key[:10]}...")
            return True
        else:
            print("❌ OpenAI API Key not found!")
            return False

