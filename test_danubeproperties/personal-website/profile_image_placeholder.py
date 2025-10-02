"""
Profile Image Placeholder Generator
This script creates a placeholder profile image for the portfolio.
Replace this with your actual profile photo.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_profile_placeholder():
    """Create a placeholder profile image with initials"""
    
    # Create a 400x400 image with blue background
    size = (400, 400)
    img = Image.new('RGB', size, color='#3498db')
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font, fallback to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 120)
        except:
            font = ImageFont.load_default()
    
    # Draw initials "AS" in white
    text = "AS"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    # Save the image
    img.save('profile_phot0.JPG.jpg', 'JPEG')
    print("Profile placeholder image created: profile_phot0.jpg")

if __name__ == "__main__":
    create_profile_placeholder()
