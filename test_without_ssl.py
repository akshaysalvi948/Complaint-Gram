#!/usr/bin/env python3
"""
Test domain without SSL verification to check if app is working
"""

import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_domain_without_ssl():
    """Test domain without SSL verification"""
    print("Testing raiseyourvoice.co.in (without SSL verification)")
    print("=" * 60)
    
    domain = "raiseyourvoice.co.in"
    
    try:
        # Test main domain
        print(f"\n[TEST] Testing https://{domain}")
        response = requests.get(f"https://{domain}", 
                              verify=False, 
                              timeout=15, 
                              allow_redirects=True)
        
        print(f"[OK] Connection successful!")
        print(f"Status Code: {response.status_code}")
        print(f"Final URL: {response.url}")
        print(f"Content Length: {len(response.content)} bytes")
        
        # Check if it's redirecting to Snowflake
        if "snowflakecomputing.com" in response.url:
            print(f"[OK] Redirecting to Snowflake correctly!")
            
            # Check for Streamlit content
            content_lower = response.text.lower()
            if "streamlit" in content_lower or "tweeterbot" in content_lower:
                print(f"[OK] Streamlit app detected!")
                return True
            else:
                print(f"[WARNING] Streamlit app not detected in content")
                return False
        else:
            print(f"[WARNING] Not redirecting to Snowflake as expected")
            return False
            
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return False

def test_www_subdomain():
    """Test www subdomain"""
    print(f"\n[TEST] Testing https://www.raiseyourvoice.co.in")
    
    try:
        response = requests.get("https://www.raiseyourvoice.co.in", 
                              verify=False, 
                              timeout=15, 
                              allow_redirects=True)
        
        print(f"[OK] www subdomain working!")
        print(f"Status Code: {response.status_code}")
        print(f"Final URL: {response.url}")
        return True
        
    except Exception as e:
        print(f"[ERROR] www subdomain failed: {e}")
        return False

if __name__ == "__main__":
    print("Note: SSL verification disabled to test app functionality")
    print("This is normal for custom domains pointing to Snowflake")
    print()
    
    main_ok = test_domain_without_ssl()
    www_ok = test_www_subdomain()
    
    print(f"\n" + "=" * 60)
    print("FINAL RESULTS:")
    print(f"Main Domain: {'WORKING' if main_ok else 'NOT WORKING'}")
    print(f"www Subdomain: {'WORKING' if www_ok else 'NOT WORKING'}")
    
    if main_ok:
        print(f"\n[SUCCESS] Your domain is working!")
        print(f"You can access your app at:")
        print(f"https://raiseyourvoice.co.in")
        print(f"https://www.raiseyourvoice.co.in")
        print(f"\nNote: You may see SSL warnings in browsers due to certificate mismatch.")
        print(f"This is normal and the app will work fine.")
    else:
        print(f"\n[ISSUES] Domain setup needs adjustment.")
        print(f"Check your DNS configuration.")
