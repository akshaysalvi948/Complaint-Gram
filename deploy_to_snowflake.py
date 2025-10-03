#!/usr/bin/env python3
"""
Snowflake Streamlit Deployment Script for TweeterBot
This script helps prepare and validate your app for Snowflake deployment
"""

import os
import sys
import json
import base64
from pathlib import Path

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"[ERROR] Missing required files: {', '.join(missing_files)}")
        return False
    
    print("[OK] All required files found")
    return True

def prepare_streamlit_app():
    """Prepare app.py for Snowflake Streamlit deployment"""
    try:
        # Read the current app.py
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create streamlit_app.py (required by Snowflake)
        with open('streamlit_app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("[OK] Created streamlit_app.py")
        return True
    except Exception as e:
        print(f"[ERROR] Error creating streamlit_app.py: {e}")
        return False

def validate_requirements():
    """Validate requirements.txt for Snowflake compatibility"""
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        # Check for Snowflake-compatible packages
        snowflake_compatible = [
            'streamlit',
            'requests',
            'Pillow',
            'pandas'
        ]
        
        incompatible = []
        for req in requirements:
            package = req.split('==')[0].split('>=')[0].split('<=')[0].strip()
            if package not in snowflake_compatible:
                incompatible.append(package)
        
        if incompatible:
            print(f"[WARNING] Potentially incompatible packages: {', '.join(incompatible)}")
            print("   These may not work in Snowflake Streamlit environment")
        
        print("[OK] Requirements.txt validated")
        return True
    except Exception as e:
        print(f"[ERROR] Error validating requirements.txt: {e}")
        return False

def create_deployment_package():
    """Create a deployment package with all necessary files"""
    try:
        # Create deployment directory
        deploy_dir = Path('snowflake_deployment')
        deploy_dir.mkdir(exist_ok=True)
        
        # Copy necessary files
        files_to_copy = [
            'app.py',
            'requirements.txt',
            '.env.example',
            'README.md'
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                try:
                    with open(file, 'r', encoding='utf-8') as src:
                        with open(deploy_dir / file, 'w', encoding='utf-8') as dst:
                            dst.write(src.read())
                except UnicodeDecodeError:
                    # Try with different encoding for binary files
                    with open(file, 'rb') as src:
                        with open(deploy_dir / file, 'wb') as dst:
                            dst.write(src.read())
        
        # Create streamlit_app.py in deployment directory
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        with open(deploy_dir / 'streamlit_app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Create deployment instructions
        instructions = """
# Snowflake Streamlit Deployment Instructions

## Files to Upload to Snowflake:
1. streamlit_app.py (main app file)
2. requirements.txt (dependencies)
3. .env.example (environment variables template)

## Steps:
1. Log into Snowflake Web Interface
2. Go to Apps → Streamlit Apps
3. Click "Create App"
4. Upload the files above
5. Configure environment variables as secrets
6. Deploy the app

## Environment Variables to Set:
- PERPLEXITY_API_KEY (required)
- HUGGINGFACE_API_KEY (optional)
- OPENAI_API_KEY (optional)
- TWITTER_API_KEY (optional)
- TWITTER_API_SECRET (optional)
- TWITTER_ACCESS_TOKEN (optional)
- TWITTER_ACCESS_TOKEN_SECRET (optional)

## SQL to Run in Snowflake:
```sql
CREATE TABLE IF NOT EXISTS TWEETERBOT_ANALYTICS (
    session_id STRING,
    action_type STRING,
    timestamp TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP(),
    image_name STRING,
    image_size INTEGER,
    ai_provider STRING,
    tweet_content STRING,
    success BOOLEAN,
    error_message STRING,
    user_agent STRING,
    ip_address STRING
);

GRANT SELECT, INSERT ON TABLE TWEETERBOT_ANALYTICS TO PUBLIC;
```

## Public Access:
After deployment, your app will be available at:
https://your-account.snowflakecomputing.com/app/TweeterBot

Share this URL with users for public access.
"""
        
        with open(deploy_dir / 'DEPLOYMENT_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"[OK] Deployment package created in '{deploy_dir}' directory")
        return True
    except Exception as e:
        print(f"[ERROR] Error creating deployment package: {e}")
        return False

def generate_sql_scripts():
    """Generate SQL scripts for Snowflake setup"""
    try:
        # Create analytics table SQL
        analytics_sql = """
-- Create TweeterBot Analytics Table
CREATE TABLE IF NOT EXISTS TWEETERBOT_ANALYTICS (
    session_id STRING,
    action_type STRING,
    timestamp TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP(),
    image_name STRING,
    image_size INTEGER,
    ai_provider STRING,
    tweet_content STRING,
    success BOOLEAN,
    error_message STRING,
    user_agent STRING,
    ip_address STRING
);

-- Grant permissions for public access
GRANT SELECT, INSERT ON TABLE TWEETERBOT_ANALYTICS TO PUBLIC;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_tweeterbot_session ON TWEETERBOT_ANALYTICS(session_id);
CREATE INDEX IF NOT EXISTS idx_tweeterbot_timestamp ON TWEETERBOT_ANALYTICS(timestamp);
CREATE INDEX IF NOT EXISTS idx_tweeterbot_action ON TWEETERBOT_ANALYTICS(action_type);
"""
        
        with open('snowflake_setup.sql', 'w', encoding='utf-8') as f:
            f.write(analytics_sql)
        
        print("[OK] Generated snowflake_setup.sql")
        return True
    except Exception as e:
        print(f"[ERROR] Error generating SQL scripts: {e}")
        return False

def main():
    """Main deployment preparation function"""
    print("Preparing TweeterBot for Snowflake Streamlit Deployment")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Prepare streamlit app
    if not prepare_streamlit_app():
        sys.exit(1)
    
    # Validate requirements
    if not validate_requirements():
        sys.exit(1)
    
    # Create deployment package
    if not create_deployment_package():
        sys.exit(1)
    
    # Generate SQL scripts
    if not generate_sql_scripts():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Deployment preparation complete!")
    print("\nNext steps:")
    print("1. Review the files in 'snowflake_deployment' directory")
    print("2. Follow the instructions in SNOWFLAKE_PUBLIC_DEPLOYMENT.md")
    print("3. Upload the files to Snowflake Streamlit Apps")
    print("4. Configure environment variables as secrets")
    print("5. Run the SQL scripts in Snowflake")
    print("6. Deploy and test your app!")
    print("\nYour app will be publicly accessible once deployed!")

if __name__ == "__main__":
    main()
