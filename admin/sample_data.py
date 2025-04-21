from models import db, Service

def create_sample_services():
    sample_services = [
        {
            'title': 'Portrait Photography',
            'description': 'Professional portrait sessions for individuals and families',
            'icon': 'fas fa-user',
            'price': '299',
            'features': '1-hour photo session, 10 professionally edited photos, Online gallery access, Print release, Location of your choice'
        },
        {
            'title': 'Event Photography',
            'description': 'Capture your special moments at weddings, parties, and corporate events',
            'icon': 'fas fa-calendar',
            'price': '499',
            'features': '4-hour coverage, 100+ professionally edited photos, Online gallery access, Print release, Second photographer available'
        },
        {
            'title': 'Landscape Photography',
            'description': 'Stunning landscape and nature photography services',
            'icon': 'fas fa-mountain',
            'price': '399',
            'features': '2-hour session, 20 high-resolution images, Online gallery access, Print release, Location scouting included'
        },
        {
            'title': 'Commercial Photography',
            'description': 'Professional product and commercial photography for businesses',
            'icon': 'fas fa-briefcase',
            'price': '599',
            'features': 'Full-day shoot, Unlimited photos, Professional lighting setup, Product styling, Commercial usage rights'
        }
    ]

    # Clear existing services
    Service.query.delete()
    
    # Add new services
    for service_data in sample_services:
        service = Service(
            title=service_data['title'],
            description=service_data['description'],
            icon=service_data['icon'],
            price=service_data['price'],
            features=service_data['features']  # This is now a comma-separated string
        )
        db.session.add(service)
    
    db.session.commit()
    print("Sample services have been added to the database.") 