#!/usr/bin/env python3
"""
Deployment validation script for TweeterBot
This script helps validate your deployment configuration before going live.
"""

import os
import sys
import importlib.util
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a required file exists"""
    if Path(filepath).exists():
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[MISSING] {description}: {filepath}")
        return False

def check_dependencies():
    """Check if all required dependencies are available"""
    required_packages = [
        'streamlit',
        'requests', 
        'pillow',
        'tweepy',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'pillow':
                import PIL
            elif package == 'python-dotenv':
                import dotenv
            else:
                importlib.import_module(package)
            print(f"[OK] {package} is installed")
        except ImportError:
            print(f"[MISSING] {package} is NOT installed")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages

def check_environment_variables():
    """Check if environment variables are set"""
    required_env_vars = [
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET', 
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET'
    ]
    
    optional_env_vars = [
        'PERPLEXITY_API_KEY',
        'HUGGINGFACE_TOKEN',
        'OPENAI_API_KEY'
    ]
    
    print("\nEnvironment Variables Check:")
    
    missing_required = []
    for var in required_env_vars:
        if os.getenv(var):
            print(f"[OK] {var} is set")
        else:
            print(f"[MISSING] {var} is NOT set")
            missing_required.append(var)
    
    print("\nOptional Environment Variables:")
    for var in optional_env_vars:
        if os.getenv(var):
            print(f"[OK] {var} is set")
        else:
            print(f"[OPTIONAL] {var} is not set")
    
    return len(missing_required) == 0, missing_required

def check_streamlit_secrets():
    """Check if Streamlit secrets file exists and is properly formatted"""
    secrets_path = Path('.streamlit/secrets.toml')
    
    if not secrets_path.exists():
        print("[INFO] Streamlit secrets file not found (okay for local development)")
        return True
    
    try:
        import toml
        secrets = toml.load(secrets_path)
        
        required_sections = ['twitter']
        required_twitter_keys = ['api_key', 'api_secret', 'access_token', 'access_token_secret']
        
        all_good = True
        
        for section in required_sections:
            if section not in secrets:
                print(f"[MISSING] Missing section [{section}] in secrets.toml")
                all_good = False
            else:
                print(f"[OK] Section [{section}] found in secrets.toml")
                
                if section == 'twitter':
                    for key in required_twitter_keys:
                        if key not in secrets[section] or not secrets[section][key]:
                            print(f"[MISSING] Missing or empty {section}.{key} in secrets.toml")
                            all_good = False
                        else:
                            print(f"[OK] {section}.{key} is configured")
        
        return all_good
        
    except ImportError:
        print("[INFO] toml package not available, cannot validate secrets format")
        return True
    except Exception as e:
        print(f"[ERROR] Error reading secrets.toml: {e}")
        return False

def main():
    """Main deployment validation function"""
    print("TweeterBot Deployment Validation")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Check required files
    print("\nFile Structure Check:")
    required_files = [
        ('app.py', 'Main application file'),
        ('requirements.txt', 'Python dependencies'),
        ('.streamlit/config.toml', 'Streamlit configuration'),
        ('README.md', 'Documentation'),
        ('DEPLOYMENT.md', 'Deployment guide')
    ]
    
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    # Check optional files
    print("\nOptional Files:")
    optional_files = [
        ('Procfile', 'Heroku deployment'),
        ('runtime.txt', 'Python version specification'),
        ('packages.txt', 'System packages for Streamlit Cloud'),
        ('.env', 'Local environment variables')
    ]
    
    for filepath, description in optional_files:
        check_file_exists(filepath, description)
    
    # Check dependencies
    print("\nDependencies Check:")
    deps_ok, missing_deps = check_dependencies()
    if not deps_ok:
        print(f"\n[ERROR] Missing dependencies: {', '.join(missing_deps)}")
        print("TIP: Run: pip install -r requirements.txt")
        all_checks_passed = False
    
    # Check environment variables
    env_ok, missing_env = check_environment_variables()
    
    # Check Streamlit secrets
    print("\nStreamlit Secrets Check:")
    secrets_ok = check_streamlit_secrets()
    
    # If either env vars OR secrets are configured, we're good
    if not env_ok and not secrets_ok:
        print(f"\n[ERROR] Missing required configuration!")
        print("Either set environment variables OR configure Streamlit secrets")
        print(f"Missing env vars: {', '.join(missing_env)}")
        print("TIP: For deployment, use Streamlit secrets in the dashboard")
        all_checks_passed = False
    elif not env_ok and secrets_ok:
        print("\n[INFO] Using Streamlit secrets for configuration (recommended for deployment)")
    elif env_ok and not secrets_ok:
        print("\n[INFO] Using environment variables for configuration")
    
    
    # Final summary
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("All checks passed! Your app is ready for deployment.")
        print("\nNext steps:")
        print("1. Push your code to GitHub")
        print("2. Deploy to Streamlit Cloud: https://share.streamlit.io")
        print("3. Add your secrets in the Streamlit Cloud dashboard")
        print("4. Test your deployed app")
    else:
        print("[ERROR] Some checks failed. Please fix the issues above before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main()
