#!/usr/bin/env python3
"""
Domain Testing Script for raiseyourvoice.co.in
Tests DNS resolution, HTTPS access, and app functionality
"""

import socket
import requests
import ssl
from urllib.parse import urlparse
import time

def test_dns_resolution(domain):
    """Test DNS resolution for the domain"""
    print(f"[TEST] Testing DNS resolution for {domain}...")
    try:
        ip_addresses = socket.gethostbyname_ex(domain)
        print(f"[OK] DNS Resolution successful!")
        print(f"   IP Addresses: {ip_addresses[2]}")
        return True
    except socket.gaierror as e:
        print(f"[ERROR] DNS Resolution failed: {e}")
        return False

def test_https_access(domain):
    """Test HTTPS access for the domain"""
    print(f"\n[TEST] Testing HTTPS access for {domain}...")
    try:
        response = requests.get(f"https://{domain}", timeout=10, allow_redirects=True)
        print(f"[OK] HTTPS Access successful!")
        print(f"   Status Code: {response.status_code}")
        print(f"   Final URL: {response.url}")
        print(f"   Content Length: {len(response.content)} bytes")
        return True
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] HTTPS Access failed: {e}")
        return False

def test_ssl_certificate(domain):
    """Test SSL certificate for the domain"""
    print(f"\n🔐 Testing SSL certificate for {domain}...")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                print(f"✅ SSL Certificate valid!")
                print(f"   Subject: {cert.get('subject', 'N/A')}")
                print(f"   Issuer: {cert.get('issuer', 'N/A')}")
                print(f"   Valid Until: {cert.get('notAfter', 'N/A')}")
                return True
    except Exception as e:
        print(f"❌ SSL Certificate test failed: {e}")
        return False

def test_app_functionality(domain):
    """Test if the app is working properly"""
    print(f"\n🚀 Testing app functionality for {domain}...")
    try:
        response = requests.get(f"https://{domain}", timeout=15, allow_redirects=True)
        
        # Check if it's redirecting to Snowflake
        if "snowflakecomputing.com" in response.url:
            print(f"✅ App redirect working!")
            print(f"   Redirected to: {response.url}")
            
            # Check if it contains Streamlit content
            if "streamlit" in response.text.lower() or "tweeterbot" in response.text.lower():
                print(f"✅ Streamlit app detected!")
                return True
            else:
                print(f"⚠️  Streamlit app not detected in content")
                return False
        else:
            print(f"⚠️  Not redirecting to Snowflake as expected")
            print(f"   Current URL: {response.url}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ App functionality test failed: {e}")
        return False

def main():
    """Main testing function"""
    print("Testing raiseyourvoice.co.in Domain Setup")
    print("=" * 50)
    
    domain = "raiseyourvoice.co.in"
    www_domain = "www.raiseyourvoice.co.in"
    
    # Test main domain
    print(f"\n📋 Testing {domain}")
    print("-" * 30)
    
    dns_ok = test_dns_resolution(domain)
    https_ok = test_https_access(domain)
    ssl_ok = test_ssl_certificate(domain)
    app_ok = test_app_functionality(domain)
    
    # Test www subdomain
    print(f"\n📋 Testing {www_domain}")
    print("-" * 30)
    
    www_dns_ok = test_dns_resolution(www_domain)
    www_https_ok = test_https_access(www_domain)
    
    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 50)
    print(f"Main Domain ({domain}):")
    print(f"  DNS Resolution: {'✅' if dns_ok else '❌'}")
    print(f"  HTTPS Access: {'✅' if https_ok else '❌'}")
    print(f"  SSL Certificate: {'✅' if ssl_ok else '❌'}")
    print(f"  App Functionality: {'✅' if app_ok else '❌'}")
    
    print(f"\nWWW Subdomain ({www_domain}):")
    print(f"  DNS Resolution: {'✅' if www_dns_ok else '❌'}")
    print(f"  HTTPS Access: {'✅' if www_https_ok else '❌'}")
    
    # Overall status
    if dns_ok and https_ok and ssl_ok and app_ok:
        print(f"\n🎉 SUCCESS! Your domain is working perfectly!")
        print(f"   Visit: https://{domain}")
        print(f"   Visit: https://{www_domain}")
    elif dns_ok and https_ok:
        print(f"\n⚠️  PARTIAL SUCCESS! DNS and HTTPS working, but app may need more time to propagate.")
        print(f"   Wait 24-48 hours for full propagation.")
    else:
        print(f"\n❌ ISSUES DETECTED! Check your DNS configuration.")
    
    print(f"\n🔗 Your Snowflake App URL:")
    print(f"   https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot")

if __name__ == "__main__":
    main()
