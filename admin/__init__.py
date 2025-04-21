from flask import Flask
from .models import db, User, Role
from .views import init_admin
import uuid

def init_app(app: Flask):
    # Initialize admin
    admin = init_admin(app)
    
    # Create admin user if it doesn't exist
    with app.app_context():
        # Create admin role if it doesn't exist
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator')
            db.session.add(admin_role)
            db.session.commit()
        
        # Create admin user if it doesn't exist
        admin_user = User.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            admin_user = User(
                email='admin@example.com',
                password='admin123',  # This will be hashed by Flask-Security
                active=True,
                fs_uniquifier=str(uuid.uuid4())
            )
            admin_user.roles.append(admin_role)
            db.session.add(admin_user)
            db.session.commit()
    
    return admin 