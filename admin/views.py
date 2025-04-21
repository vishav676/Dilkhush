from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_security import current_user, login_required
from wtforms import FileField, validators, SelectField
from .models import db, Service, PortfolioItem, User, Role
import json
import os
from flask_admin.form import FileUploadField
from werkzeug.utils import secure_filename
from flask import url_for, flash, request, current_app
import cloudinary
import cloudinary.uploader

# Custom admin index view that requires authentication
class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        return super(SecureAdminIndexView, self).index()

# Custom model views that require authentication
class SecureModelView(ModelView):
    form_base_class = SecureForm
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

# Custom service view with JSON field handling
class ServiceView(SecureModelView):
    column_list = ['title', 'description', 'icon', 'price']
    column_searchable_list = ['title', 'description']
    column_filters = ['price', 'created_at']
    form_columns = ['title', 'description', 'icon', 'price', 'features']
    
    def on_model_change(self, form, model, is_created):
        # Ensure features is a JSON string
        if isinstance(model.features, str):
            try:
                # Try to parse it as JSON to validate
                json.loads(model.features)
            except json.JSONDecodeError:
                # If it's not valid JSON, convert list to JSON string
                if isinstance(model.features, list):
                    model.features = json.dumps(model.features)
                else:
                    # If it's a string with commas, split and convert to JSON
                    model.features = json.dumps([f.strip() for f in model.features.split(',')])

# Custom portfolio view
class PortfolioView(SecureModelView):
    column_list = ['title', 'description', 'image_url', 'category']
    form_columns = ['title', 'description', 'category','image_file']
    
    # Configure file upload
    form_extra_fields = {
        'image_file': FileField('Image')
    }
    
    def on_model_change(self, form, model, is_created):
        # First, set a temporary image URL to satisfy the NOT NULL constraint
        model.image_url = "https://res.cloudinary.com/your-cloud-name/image/upload/v1/placeholder.jpg"
        
        # Then handle the file upload
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                try:
                    # Upload to Cloudinary
                    result = cloudinary.uploader.upload(file)
                    # Update the image URL with the Cloudinary URL
                    model.image_url = result['secure_url']
                    flash('Image uploaded successfully', 'success')
                except Exception as e:
                    flash(f"Image upload failed: {str(e)}", 'error')
                    raise
            else:
                flash('Please select an image file', 'error')
                raise ValueError('Image file is required')

# Initialize admin
def init_admin(app):
    admin = Admin(
        app,
        name='Portfolio Admin',
        template_mode='bootstrap4',
        index_view=SecureAdminIndexView()  # Use the secure index view
    )
    
    # Add views
    admin.add_view(ServiceView(Service, db.session))
    admin.add_view(PortfolioView(PortfolioItem, db.session))
    
    return admin 