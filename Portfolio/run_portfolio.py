#!/usr/bin/env python3
"""
Simple script to run the Streamlit portfolio application
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        print("✅ All required packages are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def run_app():
    """Run the Streamlit application"""
    if check_requirements():
        print("🚀 Starting Portfolio Application...")
        print("📱 The app will open in your browser automatically")
        print("🔗 If not, navigate to: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        print("-" * 50)
        
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", 
                "portfolio_app.py",
                "--server.headless", "false"
            ])
        except KeyboardInterrupt:
            print("\n👋 Application stopped. Thank you for using the portfolio!")
        except Exception as e:
            print(f"❌ Error running application: {e}")

if __name__ == "__main__":
    run_app()
