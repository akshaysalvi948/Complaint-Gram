#!/usr/bin/env python3
"""
Local Development Script for Portfolio
This script helps you run the portfolio locally with proper configuration.
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import streamlit
        import plotly
        import pandas
        print("✅ All requirements are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_profile_placeholder():
    """Create a profile placeholder if it doesn't exist"""
    if not os.path.exists("profile_placeholder.jpg"):
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a 400x400 image with blue background
            size = (400, 400)
            img = Image.new('RGB', size, color='#3498db')
            draw = ImageDraw.Draw(img)
            
            # Try to use a system font
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
            img.save('profile_placeholder.jpg', 'JPEG')
            print("✅ Created profile placeholder image")
        except ImportError:
            print("⚠️  Pillow not installed. Profile placeholder not created.")
        except Exception as e:
            print(f"⚠️  Could not create profile placeholder: {e}")

def run_portfolio():
    """Run the portfolio application"""
    print("🚀 Starting Portfolio Application...")
    print("📍 The app will be available at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "portfolio_app.py",
            "--server.port=8501",
            "--server.address=localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Portfolio application stopped")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main function"""
    print("🎯 Portfolio Development Helper")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Create profile placeholder
    create_profile_placeholder()
    
    # Run the application
    run_portfolio()

if __name__ == "__main__":
    main()
