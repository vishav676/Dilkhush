from app import app, db
from admin.models import User, Role, Service, PortfolioItem
from datetime import datetime
from flask_security import hash_password
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

def init_db():
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create admin role
        admin_role = Role(name='admin', description='Administrator')
        db.session.add(admin_role)
        
        # Create admin user with hashed password
        admin_user = User(
            email=os.getenv('USERNAME'),
            password=hash_password(os.getenv('PASSWORD')),  # Hash the password
            active=True,
            fs_uniquifier=str(uuid.uuid4())
        )
        admin_user.roles.append(admin_role)
        db.session.add(admin_user)
        
        # Create sample services
        sample_services = [
            Service(
                title='Portrait Photography',
                description='Professional portrait sessions for individuals and families',
                icon='fas fa-user',
                price='299',
                features='["1-hour photo session", "10 professionally edited photos", "Online gallery access", "Print release", "Location of your choice"]'
            ),
            Service(
                title='Event Photography',
                description='Capture your special moments at weddings, parties, and corporate events',
                icon='fas fa-calendar',
                price='499',
                features='["4-hour coverage", "100+ professionally edited photos", "Online gallery access", "Print release", "Second photographer available"]'
            ),
            Service(
                title='Landscape Photography',
                description='Stunning landscape and nature photography services',
                icon='fas fa-mountain',
                price='399',
                features='["2-hour session", "20 high-resolution images", "Online gallery access", "Print release", "Location scouting included"]'
            ),
            Service(
                title='Commercial Photography',
                description='Professional product and commercial photography for businesses',
                icon='fas fa-briefcase',
                price='599',
                features='["Full-day shoot", "Unlimited photos", "Professional lighting setup", "Product styling", "Commercial usage rights"]'
            )
        ]
        
        # Add services to session
        for service in sample_services:
            db.session.add(service)
        
        # Create sample portfolio items
        sample_portfolio = [
            PortfolioItem(
                title='Wedding Photography',
                description='Beautiful wedding moments captured in natural light',
                image_url='https://res.cloudinary.com/dso8uwwo1/image/upload/v1/portfolio/wedding.jpg',
                category='Wedding'
            ),
            PortfolioItem(
                title='Nature Landscape',
                description='Breathtaking landscapes from around the world',
                image_url='https://res.cloudinary.com/dso8uwwo1/image/upload/v1/portfolio/nature.jpg',
                category='Nature'
            ),
            PortfolioItem(
                title='Product Showcase',
                description='Professional product photography for e-commerce',
                image_url='https://res.cloudinary.com/dso8uwwo1/image/upload/v1/portfolio/product.jpg',
                category='Products'
            )
        ]
        
        # Add portfolio items to session
        for item in sample_portfolio:
            db.session.add(item)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized successfully with sample data!")

if __name__ == '__main__':
    init_db() 