#!/usr/bin/env python3
"""
Simple Domain Testing Script for raiseyourvoice.co.in
"""

import socket
import requests

def test_domain():
    """Test the domain setup"""
    print("Testing raiseyourvoice.co.in Domain Setup")
    print("=" * 50)
    
    domain = "raiseyourvoice.co.in"
    
    # Test 1: DNS Resolution
    print(f"\n[TEST 1] DNS Resolution for {domain}")
    try:
        ip_addresses = socket.gethostbyname_ex(domain)
        print(f"[OK] DNS working! IPs: {ip_addresses[2]}")
        dns_ok = True
    except Exception as e:
        print(f"[ERROR] DNS failed: {e}")
        dns_ok = False
    
    # Test 2: HTTPS Access
    print(f"\n[TEST 2] HTTPS Access for {domain}")
    try:
        response = requests.get(f"https://{domain}", timeout=10, allow_redirects=True)
        print(f"[OK] HTTPS working! Status: {response.status_code}")
        print(f"Final URL: {response.url}")
        https_ok = True
    except Exception as e:
        print(f"[ERROR] HTTPS failed: {e}")
        https_ok = False
    
    # Test 3: www subdomain
    print(f"\n[TEST 3] www subdomain test")
    try:
        www_response = requests.get(f"https://www.{domain}", timeout=10, allow_redirects=True)
        print(f"[OK] www subdomain working! Status: {www_response.status_code}")
        www_ok = True
    except Exception as e:
        print(f"[ERROR] www subdomain failed: {e}")
        www_ok = False
    
    # Summary
    print(f"\n" + "=" * 50)
    print("TEST SUMMARY:")
    print(f"DNS Resolution: {'PASS' if dns_ok else 'FAIL'}")
    print(f"HTTPS Access: {'PASS' if https_ok else 'FAIL'}")
    print(f"www Subdomain: {'PASS' if www_ok else 'FAIL'}")
    
    if dns_ok and https_ok:
        print(f"\n[SUCCESS] Your domain is working!")
        print(f"Visit: https://{domain}")
        print(f"Visit: https://www.{domain}")
    else:
        print(f"\n[ISSUES] Some tests failed. Check DNS configuration.")
    
    print(f"\nYour Snowflake App URL:")
    print(f"https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot")

if __name__ == "__main__":
    test_domain()
