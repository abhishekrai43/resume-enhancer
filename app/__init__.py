from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

# ✅ Initialize extensions globally (do not create a new instance in other files)
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # ✅ Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, supports_credentials=True, origins=["http://localhost:4200"])

    # ✅ Push app context globally to prevent "None" errors
    
    with app.app_context():
        db.create_all()

    # ✅ Register Blueprints
    from app.routes.auth_routes import auth_routes
    from app.routes.resume_routes import resume_routes
    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(resume_routes, url_prefix="/resume")

    return app

# ✅ Push the app context at the global level when Flask starts
app = create_app()
app.app_context().push()  # ⬅️ This ensures all db.session calls are in context
