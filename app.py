from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
import os
from datetime import datetime
from admin.models import db
from flask_migrate import Migrate
import cloudinary
import cloudinary.uploader
from flask_security import Security, SQLAlchemySessionUserDatastore
from admin.models import User, Role
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

# Configure Flask
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Security configuration
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('FLASK_SECURITY_PASSWORD_SALT')
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_REGISTERABLE'] = False
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_USERNAME_ENABLE'] = False
app.config['SECURITY_USERNAME_REQUIRED'] = False
app.config['SECURITY_URL_PREFIX'] = '/admin'
app.config['SECURITY_LOGIN_URL'] = '/login'
app.config['SECURITY_LOGOUT_URL'] = '/logout'
app.config['SECURITY_POST_LOGIN_VIEW'] = '/admin/'
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/admin/'

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)

# Import and initialize admin after db is initialized
from admin import init_app
init_app(app)

# Sample data for services (fallback if database is empty)
SAMPLE_SERVICES = [
    {
        'title': 'Portrait Photography',
        'description': 'Professional portrait sessions for individuals and families',
        'icon': 'fas fa-user',
        'price': '299',
        'features': [
            '1-hour photo session',
            '10 professionally edited photos',
            'Online gallery access',
            'Print release',
            'Location of your choice'
        ]
    },
    {
        'title': 'Event Photography',
        'description': 'Capture your special moments at weddings, parties, and corporate events',
        'icon': 'fas fa-calendar',
        'price': '499',
        'features': [
            '4-hour coverage',
            '100+ professionally edited photos',
            'Online gallery access',
            'Print release',
            'Second photographer available'
        ]
    },
    {
        'title': 'Landscape Photography',
        'description': 'Stunning landscape and nature photography services',
        'icon': 'fas fa-mountain',
        'price': '399',
        'features': [
            '2-hour session',
            '20 high-resolution images',
            'Online gallery access',
            'Print release',
            'Location scouting included'
        ]
    },
    {
        'title': 'Commercial Photography',
        'description': 'Professional product and commercial photography for businesses',
        'icon': 'fas fa-briefcase',
        'price': '599',
        'features': [
            'Full-day shoot',
            'Unlimited photos',
            'Professional lighting setup',
            'Product styling',
            'Commercial usage rights'
        ]
    }
]

# Sample categories for portfolio
categories = [
    {
        'name': 'Portrait',
        'slug': 'portrait'
    },
    {
        'name': 'Landscape',
        'slug': 'landscape'
    },
    {
        'name': 'Event',
        'slug': 'event'
    },
    {
        'name': 'Commercial',
        'slug': 'commercial'
    }
]

@app.route('/')
def home():
    from admin.models import Service, PortfolioItem
    # Try to get services from database, fallback to sample data
    try:
        services = Service.query.all()
        if not services:
            services = SAMPLE_SERVICES
    except:
        services = SAMPLE_SERVICES
    
    # Try to get portfolio items from database
    try:
        portfolio_items = PortfolioItem.query.all()
    except:
        portfolio_items = []
    
    return render_template('index.html', services=services, portfolio_items=portfolio_items)

@app.route('/services')
def services_page():
    from admin.models import Service
    # Try to get services from database, fallback to sample data
    try:
        services = Service.query.all()
        if not services:
            services = SAMPLE_SERVICES
    except:
        services = SAMPLE_SERVICES
    
    return render_template('services.html', services=services)

@app.route('/portfolio')
def portfolio_page():
    from admin.models import PortfolioItem
    try:
        portfolio_items = PortfolioItem.query.all()
    except:
        portfolio_items = []
    
    return render_template('portfolio.html', portfolio_items=portfolio_items, categories=categories)

@app.route('/contact')
def contact():
    from admin.models import Service
    selected_service_title = request.args.get('service', '')
    # Try to get services from database, fallback to sample data
    try:
        services = Service.query.all()
        if not services:
            services = SAMPLE_SERVICES
    except:
        services = SAMPLE_SERVICES
    
    # Find the selected service
    selected_service = None
    if selected_service_title:
        for service in services:
            if service.title == selected_service_title:
                selected_service = service
                break
    
    # Get today's date in YYYY-MM-DD format
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('contact.html', 
                         services=services, 
                         selected_service=selected_service_title,
                         selected_service_description=selected_service.description if selected_service else '',
                         selected_service_price=selected_service.price if selected_service else '',
                         selected_service_features=selected_service.features_list if selected_service else [],
                         today=today)

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    service = request.form.get('service')
    date = request.form.get('date')
    message = request.form.get('message')

    # Here you would typically:
    # 1. Validate the form data
    # 2. Store the booking in a database
    # 3. Send confirmation emails
    # 4. Handle any errors

    # For now, we'll just show a success message
    flash('Your booking has been submitted successfully! We will contact you shortly.', 'success')
    return redirect(url_for('contact'))

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the app
    if os.getenv('FLASK_ENV') == 'production':
        # In production, use the port provided by Render
        port = int(os.getenv('PORT', 10000))
        app.run(host='0.0.0.0', port=port)
    else:
        # In development, use the default port
        app.run(debug=True) 