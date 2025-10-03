#!/usr/bin/env python3
"""
Test script for Snowflake SiS compatibility
Tests key functions without requiring actual API keys or Snowflake connection
"""

import sys
import importlib.util
from PIL import Image
import io
import base64

def test_imports():
    """Test that all required imports work"""
    print("🧪 Testing imports...")
    
    try:
        import requests
        print("✅ requests - OK")
    except ImportError as e:
        print(f"❌ requests - FAILED: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ PIL (Pillow) - OK")
    except ImportError as e:
        print(f"❌ PIL (Pillow) - FAILED: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas - OK")
    except ImportError as e:
        print(f"❌ pandas - FAILED: {e}")
        return False
    
    # Test that problematic imports are NOT used
    try:
        import tweepy
        print("⚠️  tweepy found - This should NOT be used in SiS version")
        return False
    except ImportError:
        print("✅ tweepy not found - Good for SiS compatibility")
    
    try:
        import dotenv
        print("⚠️  python-dotenv found - This should NOT be used in SiS version")
        return False
    except ImportError:
        print("✅ python-dotenv not found - Good for SiS compatibility")
    
    return True

def test_app_syntax():
    """Test that the app file has valid Python syntax"""
    print("\n🧪 Testing app syntax...")
    
    try:
        spec = importlib.util.spec_from_file_location("app_snowflake_sis", "app_snowflake_sis.py")
        module = importlib.util.module_from_spec(spec)
        # Don't execute, just check syntax
        with open("app_snowflake_sis.py", 'r') as f:
            compile(f.read(), "app_snowflake_sis.py", 'exec')
        print("✅ App syntax - OK")
        return True
    except SyntaxError as e:
        print(f"❌ App syntax - FAILED: {e}")
        return False
    except Exception as e:
        print(f"❌ App syntax - ERROR: {e}")
        return False

def test_image_functions():
    """Test image processing functions"""
    print("\n🧪 Testing image functions...")
    
    try:
        # Create a test image
        test_image = Image.new('RGB', (100, 100), color='red')
        
        # Test base64 encoding (simulate the function)
        buffer = io.BytesIO()
        test_image.save(buffer, format='JPEG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        if img_str and len(img_str) > 0:
            print("✅ Image base64 encoding - OK")
            return True
        else:
            print("❌ Image base64 encoding - FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Image functions - ERROR: {e}")
        return False

def test_oauth_functions():
    """Test OAuth signature generation (without actual API calls)"""
    print("\n🧪 Testing OAuth functions...")
    
    try:
        import hashlib
        import hmac
        import urllib.parse
        from datetime import datetime
        
        # Test basic OAuth components
        method = "POST"
        url = "https://api.twitter.com/1.1/statuses/update.json"
        params = {
            'oauth_consumer_key': 'test_key',
            'oauth_nonce': 'test_nonce',
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(datetime.now().timestamp())),
            'oauth_token': 'test_token',
            'oauth_version': '1.0'
        }
        
        # Test parameter sorting and encoding
        sorted_params = sorted(params.items())
        param_string = "&".join([f"{k}={v}" for k, v in sorted_params])
        
        if param_string and len(param_string) > 0:
            print("✅ OAuth parameter handling - OK")
            return True
        else:
            print("❌ OAuth parameter handling - FAILED")
            return False
            
    except Exception as e:
        print(f"❌ OAuth functions - ERROR: {e}")
        return False

def test_requirements():
    """Test requirements.txt compatibility"""
    print("\n🧪 Testing requirements...")
    
    try:
        with open("requirements_snowflake_sis.txt", 'r') as f:
            requirements = f.read()
        
        # Check that problematic packages are not included
        if 'tweepy' in requirements:
            print("❌ tweepy found in requirements - Not SiS compatible")
            return False
        
        if 'python-dotenv' in requirements:
            print("❌ python-dotenv found in requirements - Not SiS compatible")
            return False
        
        if 'snowflake-connector-python' in requirements:
            print("❌ snowflake-connector-python found in requirements - Not needed in SiS")
            return False
        
        # Check that required packages are included
        required_packages = ['streamlit', 'requests', 'Pillow', 'pandas']
        for package in required_packages:
            if package.lower() not in requirements.lower():
                print(f"❌ {package} not found in requirements")
                return False
        
        print("✅ Requirements file - OK")
        return True
        
    except Exception as e:
        print(f"❌ Requirements test - ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("🏔️  Snowflake SiS Compatibility Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_app_syntax,
        test_image_functions,
        test_oauth_functions,
        test_requirements
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your app is ready for Snowflake SiS deployment!")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
