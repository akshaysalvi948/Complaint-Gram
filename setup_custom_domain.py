#!/usr/bin/env python3
"""
Custom Domain Setup Script for Snowflake Streamlit TweeterBot
This script helps configure your GoDaddy domain for Snowflake Streamlit app
"""

import os
import sys
import json
from pathlib import Path

def get_snowflake_info():
    """Get Snowflake app information from user"""
    print("=== Snowflake Streamlit App Information ===")
    
    snowflake_account = input("Enter your Snowflake account name (e.g., 'abc12345'): ").strip()
    if not snowflake_account:
        print("[ERROR] Snowflake account name is required")
        return None
    
    app_name = input("Enter your Streamlit app name (e.g., 'TweeterBot'): ").strip()
    if not app_name:
        print("[ERROR] App name is required")
        return None
    
    # Construct the Snowflake URL
    snowflake_url = f"https://{snowflake_account}.snowflakecomputing.com/app/{app_name}"
    
    print(f"\n[INFO] Your Snowflake app URL: {snowflake_url}")
    
    return {
        'account': snowflake_account,
        'app_name': app_name,
        'url': snowflake_url
    }

def get_domain_info():
    """Get domain information from user"""
    print("\n=== Domain Information ===")
    
    domain = input("Enter your domain name (e.g., 'tweeterbot.com'): ").strip()
    if not domain:
        print("[ERROR] Domain name is required")
        return None
    
    # Remove protocol if included
    domain = domain.replace('https://', '').replace('http://', '').replace('www.', '')
    
    print(f"\n[INFO] Domain: {domain}")
    print(f"[INFO] www subdomain: www.{domain}")
    
    return {
        'domain': domain,
        'www_domain': f"www.{domain}"
    }

def generate_dns_config(snowflake_info, domain_info):
    """Generate DNS configuration for GoDaddy"""
    print("\n=== GoDaddy DNS Configuration ===")
    
    config = f"""
# DNS Records to Add in GoDaddy

## CNAME Records
Type: CNAME
Name: @
Value: {snowflake_info['account']}.snowflakecomputing.com
TTL: 600

Type: CNAME
Name: www
Value: {snowflake_info['account']}.snowflakecomputing.com
TTL: 600

## A Records (Alternative - if CNAME doesn't work)
Type: A
Name: @
Value: [Get IP from: nslookup {snowflake_info['account']}.snowflakecomputing.com]
TTL: 600

Type: A
Name: www
Value: [Get IP from: nslookup {snowflake_info['account']}.snowflakecomputing.com]
TTL: 600
"""
    
    print(config)
    return config

def generate_cloudflare_config(snowflake_info, domain_info):
    """Generate Cloudflare configuration"""
    print("\n=== Cloudflare Configuration (Alternative Method) ===")
    
    config = f"""
# Cloudflare DNS Records

## CNAME Records
Type: CNAME
Name: @
Target: {snowflake_info['account']}.snowflakecomputing.com
Proxy status: Proxied (orange cloud)

Type: CNAME
Name: www
Target: {snowflake_info['account']}.snowflakecomputing.com
Proxy status: Proxied (orange cloud)

## Page Rules
URL: {domain_info['domain']}/*
Setting: Forwarding URL (301 redirect)
Destination: {snowflake_info['url']}

URL: www.{domain_info['domain']}/*
Setting: Forwarding URL (301 redirect)
Destination: {snowflake_info['url']}

## SSL/TLS Settings
- Encryption mode: Full
- Always Use HTTPS: Enabled
- HTTP Strict Transport Security (HSTS): Enabled
"""
    
    print(config)
    return config

def generate_nginx_config(snowflake_info, domain_info):
    """Generate Nginx configuration for reverse proxy"""
    print("\n=== Nginx Configuration (VPS Method) ===")
    
    config = f"""
# Nginx Configuration for /etc/nginx/sites-available/{domain_info['domain']}

server {{
    listen 80;
    server_name {domain_info['domain']} www.{domain_info['domain']};
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name {domain_info['domain']} www.{domain_info['domain']};
    
    # SSL Configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/{domain_info['domain']}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain_info['domain']}/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Proxy to Snowflake
    location / {{
        proxy_pass {snowflake_info['url']};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }}
}}
"""
    
    print(config)
    return config

def generate_test_commands(domain_info):
    """Generate commands to test domain configuration"""
    print("\n=== Testing Commands ===")
    
    commands = f"""
# Test DNS Resolution
nslookup {domain_info['domain']}
nslookup www.{domain_info['domain']}

# Test HTTP/HTTPS
curl -I http://{domain_info['domain']}
curl -I https://{domain_info['domain']}

# Test Redirect
curl -L https://{domain_info['domain']}

# Check SSL Certificate
openssl s_client -connect {domain_info['domain']}:443 -servername {domain_info['domain']}

# Browser Testing
# Open in browser: https://{domain_info['domain']}
# Check browser console for errors
# Test image upload functionality
"""
    
    print(commands)
    return commands

def save_configurations(snowflake_info, domain_info, dns_config, cloudflare_config, nginx_config, test_commands):
    """Save all configurations to files"""
    try:
        # Create domain setup directory
        setup_dir = Path('domain_setup')
        setup_dir.mkdir(exist_ok=True)
        
        # Save DNS configuration
        with open(setup_dir / 'godaddy_dns_config.txt', 'w') as f:
            f.write(dns_config)
        
        # Save Cloudflare configuration
        with open(setup_dir / 'cloudflare_config.txt', 'w') as f:
            f.write(cloudflare_config)
        
        # Save Nginx configuration
        with open(setup_dir / 'nginx_config.conf', 'w') as f:
            f.write(nginx_config)
        
        # Save test commands
        with open(setup_dir / 'test_commands.txt', 'w') as f:
            f.write(test_commands)
        
        # Save domain info
        domain_data = {
            'domain': domain_info['domain'],
            'snowflake_account': snowflake_info['account'],
            'snowflake_app': snowflake_info['app_name'],
            'snowflake_url': snowflake_info['url']
        }
        
        with open(setup_dir / 'domain_info.json', 'w') as f:
            json.dump(domain_data, f, indent=2)
        
        print(f"\n[OK] Configuration files saved to '{setup_dir}' directory")
        return True
    except Exception as e:
        print(f"[ERROR] Error saving configurations: {e}")
        return False

def main():
    """Main domain setup function"""
    print("Custom Domain Setup for Snowflake Streamlit TweeterBot")
    print("=" * 60)
    
    # Get Snowflake information
    snowflake_info = get_snowflake_info()
    if not snowflake_info:
        sys.exit(1)
    
    # Get domain information
    domain_info = get_domain_info()
    if not domain_info:
        sys.exit(1)
    
    # Generate configurations
    print("\n" + "=" * 60)
    print("Generating configurations...")
    
    dns_config = generate_dns_config(snowflake_info, domain_info)
    cloudflare_config = generate_cloudflare_config(snowflake_info, domain_info)
    nginx_config = generate_nginx_config(snowflake_info, domain_info)
    test_commands = generate_test_commands(domain_info)
    
    # Save configurations
    if not save_configurations(snowflake_info, domain_info, dns_config, cloudflare_config, nginx_config, test_commands):
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Domain setup configuration complete!")
    print("\nNext steps:")
    print("1. Choose your preferred method:")
    print("   - Method 1: Direct DNS (GoDaddy) - Use godaddy_dns_config.txt")
    print("   - Method 2: Cloudflare Proxy - Use cloudflare_config.txt")
    print("   - Method 3: VPS Reverse Proxy - Use nginx_config.conf")
    print("2. Follow the configuration steps")
    print("3. Test using the commands in test_commands.txt")
    print("4. Wait for DNS propagation (24-48 hours)")
    print("5. Your app will be available at: https://" + domain_info['domain'])
    print("\nFor detailed instructions, see CUSTOM_DOMAIN_SETUP.md")

if __name__ == "__main__":
    main()
