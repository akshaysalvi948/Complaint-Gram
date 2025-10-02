#!/usr/bin/env python3
"""
Setup Script for Portfolio
This script helps set up the portfolio project for the first time.
"""

import os
import sys
import subprocess

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("🎯 AKSHAY SALVI - SENIOR DATA ENGINEER PORTFOLIO")
    print("=" * 60)
    print("🚀 Setting up your professional portfolio...")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_profile_placeholder():
    """Create profile placeholder image"""
    print("🖼️  Creating profile placeholder...")
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
        print("✅ Profile placeholder created")
        return True
    except ImportError:
        print("⚠️  Pillow not available. Install with: pip install Pillow")
        return False
    except Exception as e:
        print(f"⚠️  Could not create profile placeholder: {e}")
        return False

def test_application():
    """Test if the application can start"""
    print("🧪 Testing application...")
    try:
        # Import the main modules
        import streamlit
        import plotly
        import pandas
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("1. Add your profile photo as 'profile_photo.jpg' (optional)")
    print("2. Customize your information in 'portfolio_app.py'")
    print("3. Test locally: python run_local.py")
    print("4. Deploy to GitHub and Streamlit Cloud")
    print()
    print("🚀 Quick Start:")
    print("   python run_local.py")
    print()
    print("📚 Documentation:")
    print("   - README.md - Complete guide")
    print("   - DEPLOYMENT.md - Deployment instructions")
    print()
    print("🔗 Useful Links:")
    print("   - Streamlit Community Cloud: https://share.streamlit.io/")
    print("   - Streamlit Docs: https://docs.streamlit.io/")
    print()
    print("💡 Tips:")
    print("   - Replace 'profile_placeholder.jpg' with your actual photo")
    print("   - Update personal information in portfolio_app.py")
    print("   - Customize colors and styling in the CSS section")
    print()
    print("Happy coding! 🚀")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Create profile placeholder
    create_profile_placeholder()
    
    # Test application
    if not test_application():
        return
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
