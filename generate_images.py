from PIL import Image, ImageDraw, ImageFont
import os

# Create images directory if it doesn't exist
os.makedirs('static/images', exist_ok=True)

# Sample images to generate
images = [
    {
        'filename': 'portrait1.jpg',
        'text': 'Portrait Photography',
        'color': (52, 152, 219)  # Blue
    },
    {
        'filename': 'landscape1.jpg',
        'text': 'Landscape Photography',
        'color': (46, 204, 113)  # Green
    },
    {
        'filename': 'event1.jpg',
        'text': 'Event Photography',
        'color': (155, 89, 182)  # Purple
    },
    {
        'filename': 'hero-bg.jpg',
        'text': 'Photography Portfolio',
        'color': (44, 62, 80)  # Dark Blue
    }
]

# Generate each image
for img in images:
    # Create a new image with a solid color
    image = Image.new('RGB', (800, 600), img['color'])
    draw = ImageDraw.Draw(image)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = img['text']
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (800 - text_width) // 2
    y = (600 - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    # Save the image
    image.save(f'static/images/{img["filename"]}')

print("Sample images generated successfully!") 