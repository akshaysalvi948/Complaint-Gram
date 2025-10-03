# 🌐 Your Custom Domain Setup Guide

## Your Snowflake Details
- **Account**: GMOFVVK-QA77419
- **App URL**: https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot
- **Database**: TWEETERBOT_DB
- **Schema**: TWEET_DATA
- **User**: akshaycdac948

## 🚀 Method 1: GoDaddy DNS (Easiest)

### Step 1: Log into GoDaddy
1. Go to [https://dcc.godaddy.com](https://dcc.godaddy.com)
2. Sign in with your GoDaddy account
3. Find your domain and click **"DNS"**

### Step 2: Add DNS Records
Add these **CNAME records**:

```
Record 1:
Type: CNAME
Name: @
Value: GMOFVVK-QA77419.snowflakecomputing.com
TTL: 600

Record 2:
Type: CNAME
Name: www
Value: GMOFVVK-QA77419.snowflakecomputing.com
TTL: 600
```

### Step 3: Wait and Test
- Wait 24-48 hours for DNS propagation
- Test: `https://yourdomain.com`
- Should redirect to your Snowflake app

---

## 🔧 Method 2: Cloudflare (Recommended)

### Step 1: Set up Cloudflare
1. Go to [https://cloudflare.com](https://cloudflare.com)
2. Sign up for **free account**
3. Click **"Add a Site"**
4. Enter your domain name
5. Select **"Free"** plan

### Step 2: Update Nameservers in GoDaddy
1. Cloudflare will give you nameservers like:
   - `ns1.cloudflare.com`
   - `ns2.cloudflare.com`
2. In GoDaddy, go to **"Nameservers"**
3. Change to **"Custom"**
4. Enter Cloudflare nameservers

### Step 3: Configure DNS in Cloudflare
Add these records:

```
Record 1:
Type: CNAME
Name: @
Target: GMOFVVK-QA77419.snowflakecomputing.com
Proxy: ON (orange cloud)

Record 2:
Type: CNAME
Name: www
Target: GMOFVVK-QA77419.snowflakecomputing.com
Proxy: ON (orange cloud)
```

### Step 4: Set up Redirects
Go to **"Rules"** → **"Page Rules"**:

```
Rule 1:
URL: yourdomain.com/*
Setting: Forwarding URL (301)
Destination: https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot

Rule 2:
URL: www.yourdomain.com/*
Setting: Forwarding URL (301)
Destination: https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot
```

### Step 5: Enable SSL
1. Go to **"SSL/TLS"** → **"Overview"**
2. Set encryption to **"Full"**
3. Go to **"SSL/TLS"** → **"Edge Certificates"**
4. Enable **"Always Use HTTPS"**

---

## 🖥️ Method 3: VPS with Nginx (Advanced)

### Step 1: Get a VPS
- **DigitalOcean**: $5/month droplet
- **Linode**: $5/month instance
- **AWS EC2**: $5-10/month

### Step 2: Install Nginx
```bash
sudo apt update
sudo apt install nginx
```

### Step 3: Configure Nginx
1. Create config file:
   ```bash
   sudo nano /etc/nginx/sites-available/yourdomain.com
   ```
2. Copy the configuration from `nginx_config.conf`
3. Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/
   ```

### Step 4: Set up SSL
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Step 5: Test and Restart
```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🧪 Testing Your Domain

### Quick Tests
```bash
# Test DNS resolution
nslookup yourdomain.com

# Test HTTPS
curl -I https://yourdomain.com

# Test redirect
curl -L https://yourdomain.com
```

### Browser Tests
1. Open `https://yourdomain.com`
2. Upload an image
3. Generate a tweet
4. Verify all features work

---

## ⚡ Quick Start (Choose One Method)

### Option A: GoDaddy DNS (5 minutes)
1. Add CNAME records in GoDaddy
2. Wait 24-48 hours
3. Test your domain

### Option B: Cloudflare (15 minutes)
1. Add domain to Cloudflare
2. Update nameservers in GoDaddy
3. Configure DNS and redirects
4. Enable SSL
5. Test immediately

### Option C: VPS (30 minutes)
1. Get VPS and install Nginx
2. Configure reverse proxy
3. Set up SSL certificate
4. Test and go live

---

## 🎯 Recommended: Cloudflare Method

**Why Cloudflare?**
- ✅ Free SSL certificate
- ✅ Faster loading times
- ✅ Better security
- ✅ Easy DNS management
- ✅ Works immediately

**Steps:**
1. Add domain to Cloudflare
2. Update nameservers in GoDaddy
3. Configure DNS records
4. Set up redirects
5. Enable SSL
6. Test your domain!

---

## 🆘 Troubleshooting

### Domain Not Working?
- Check DNS propagation: [https://dnschecker.org](https://dnschecker.org)
- Verify CNAME records are correct
- Wait 24-48 hours for full propagation

### SSL Issues?
- Check Cloudflare SSL settings
- Ensure "Always Use HTTPS" is enabled
- Clear browser cache

### App Not Loading?
- Test Snowflake app directly: https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot
- Check proxy configuration
- Verify redirects are set up correctly

---

## 🎉 Success!

Once configured, your TweeterBot will be available at:
**`https://yourdomain.com`**

Share this URL with users and they can access your AI-powered image-to-tweet generator from your custom domain! 🚀
