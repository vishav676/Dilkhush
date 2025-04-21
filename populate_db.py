from app import app
from admin.sample_data import create_sample_services

with app.app_context():
    create_sample_services()
    print("Database has been populated with sample data.") 