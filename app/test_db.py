from app import create_app, db
from sqlalchemy.sql import text  # Import `text` to construct SQL statements

# Create the app and test database connection
app = create_app()

with app.app_context():
    try:
        # Use the connection from the engine to execute a query
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!", result.fetchone())
    except Exception as e:
        print(f"Database connection failed: {e}")
