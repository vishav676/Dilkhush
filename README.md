# Photography Portfolio Website

A beautiful, responsive photography portfolio website built with Flask and Bootstrap.

## Features

- Responsive design that works on all devices
- Modern and clean UI
- Services showcase
- Portfolio gallery
- Contact form
- Social media integration

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create the following directory structure:
```
your_project/
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│       ├── hero-bg.jpg
│       ├── placeholder1.jpg
│       ├── placeholder2.jpg
│       └── placeholder3.jpg
├── templates/
│   └── index.html
├── app.py
└── requirements.txt
```

5. Add your own images to the `static/images` directory:
- hero-bg.jpg (for the hero section background)
- placeholder1.jpg, placeholder2.jpg, placeholder3.jpg (for portfolio items)

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application:
```bash
python app.py
```
3. Open your browser and navigate to `http://localhost:5000`

## Customization

- Replace the placeholder images with your own photography
- Modify the services in `app.py` to match your offerings
- Update the contact form to connect to your email service
- Add your social media links in the footer
- Customize colors and styles in `static/css/style.css`

## Technologies Used

- Flask (Python web framework)
- Bootstrap 5 (Frontend framework)
- Font Awesome (Icons)
- Custom CSS 