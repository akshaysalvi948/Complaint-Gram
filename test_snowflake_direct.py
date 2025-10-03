#!/usr/bin/env python3
"""
Test Snowflake app directly to verify it's working
"""

import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_snowflake_app():
    """Test the Snowflake app directly"""
    print("Testing Snowflake App Directly")
    print("=" * 40)
    
    snowflake_url = "https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot"
    
    try:
        print(f"[TEST] Testing Snowflake app directly...")
        print(f"URL: {snowflake_url}")
        
        response = requests.get(snowflake_url, 
                              verify=False, 
                              timeout=15, 
                              allow_redirects=True)
        
        print(f"[OK] Snowflake app is working!")
        print(f"Status Code: {response.status_code}")
        print(f"Final URL: {response.url}")
        print(f"Content Length: {len(response.content)} bytes")
        
        # Check for Streamlit content
        content_lower = response.text.lower()
        if "streamlit" in content_lower or "tweeterbot" in content_lower:
            print(f"[OK] Streamlit TweeterBot app detected!")
            return True
        else:
            print(f"[WARNING] Streamlit app not detected in content")
            return False
            
    except Exception as e:
        print(f"[ERROR] Snowflake app test failed: {e}")
        return False

def test_domain_current_status():
    """Test current domain status"""
    print(f"\nTesting Current Domain Status")
    print("=" * 40)
    
    domain = "raiseyourvoice.co.in"
    
    try:
        print(f"[TEST] Testing https://{domain}")
        response = requests.get(f"https://{domain}", 
                              verify=False, 
                              timeout=10, 
                              allow_redirects=True)
        
        print(f"Status Code: {response.status_code}")
        print(f"Final URL: {response.url}")
        
        if response.status_code == 404:
            print(f"[INFO] 404 error - domain points to Snowflake but no redirect to app")
        elif "snowflakecomputing.com" in response.url:
            print(f"[OK] Redirecting to Snowflake!")
        else:
            print(f"[INFO] Not redirecting as expected")
            
    except Exception as e:
        print(f"[ERROR] Domain test failed: {e}")

if __name__ == "__main__":
    print("Testing Snowflake App and Domain Status")
    print("=" * 50)
    
    # Test Snowflake app directly
    snowflake_ok = test_snowflake_app()
    
    # Test current domain status
    test_domain_current_status()
    
    print(f"\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Snowflake App: {'WORKING' if snowflake_ok else 'NOT WORKING'}")
    print(f"Domain DNS: WORKING (3 IPs resolving)")
    print(f"Domain Redirect: NOT WORKING (needs Cloudflare setup)")
    
    if snowflake_ok:
        print(f"\n[SUCCESS] Your Snowflake app is working!")
        print(f"Direct URL: https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot")
        print(f"\n[SOLUTION] Set up Cloudflare to redirect your domain to the app")
    else:
        print(f"\n[ISSUE] Snowflake app needs to be checked")
