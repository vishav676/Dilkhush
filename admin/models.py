from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

# Define the Role data model
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# Define the User data model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)  # Required for Flask-Security 4.0.0
    roles = db.relationship('Role', secondary='user_roles',
                          backref=db.backref('users', lazy='dynamic'))

# Define the UserRoles association table
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

# Define the Service data model
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    features = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @hybrid_property
    def features_list(self):
        if isinstance(self.features, str):
            # Remove any quotes and brackets, then split by comma
            cleaned = self.features.replace('"', '').replace('[', '').replace(']', '')
            return [feature.strip() for feature in cleaned.split(',')]
        return self.features

    @features_list.setter
    def features_list(self, value):
        if isinstance(value, list):
            self.features = ','.join(value)
        else:
            self.features = value

    def __repr__(self):
        return f'<Service {self.title}>'

# Define the PortfolioItem data model
class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PortfolioItem {self.title}>' 