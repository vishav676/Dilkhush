from app import app, db, init_db
from flask_migrate import upgrade

# Initialize the database
with app.app_context():
    # Run migrations
    upgrade()
    # Initialize database and create roles
    init_db()

if __name__ == "__main__":
    app.run() 