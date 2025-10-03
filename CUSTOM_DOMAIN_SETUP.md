# 🌐 Custom Domain Setup for Snowflake Streamlit App

This guide will help you connect your GoDaddy domain to your Snowflake Streamlit TweeterBot application.

## 📋 Prerequisites

- ✅ **GoDaddy Domain**: Your domain purchased from GoDaddy
- ✅ **Snowflake Streamlit App**: Your TweeterBot app already deployed
- ✅ **Domain Access**: Ability to modify DNS settings in GoDaddy
- ✅ **Snowflake Account**: Admin access to your Snowflake account

## 🚀 Step-by-Step Setup

### Step 1: Get Your Snowflake App URL

1. **Log into Snowflake**
   - Go to [https://app.snowflake.com](https://app.snowflake.com)
   - Navigate to **Apps** → **Streamlit Apps**
   - Find your TweeterBot app

2. **Copy the App URL**
   - Your app URL will look like: `https://your-account.snowflakecomputing.com/app/TweeterBot`
   - Copy this URL - you'll need it for DNS configuration

### Step 2: Configure DNS in GoDaddy

1. **Log into GoDaddy**
   - Go to [https://dcc.godaddy.com](https://dcc.godaddy.com)
   - Sign in with your GoDaddy account

2. **Access DNS Management**
   - Find your domain in the list
   - Click **"DNS"** or **"Manage DNS"**

3. **Add CNAME Record**
   - Click **"Add"** or **"Add Record"**
   - Select **"CNAME"** as the record type
   - Fill in the following:
     ```
     Type: CNAME
     Name: @ (or leave blank for root domain)
     Value: your-account.snowflakecomputing.com
     TTL: 600 (or 1 hour)
     ```
   - Click **"Save"**

4. **Add www Subdomain (Optional)**
   - Add another CNAME record:
     ```
     Type: CNAME
     Name: www
     Value: your-account.snowflakecomputing.com
     TTL: 600
     ```

### Step 3: Configure Snowflake for Custom Domain

1. **Contact Snowflake Support**
   - Email: support@snowflake.com
   - Subject: "Custom Domain Setup for Streamlit App"
   - Include:
     - Your domain name
     - Your Snowflake account name
     - Your Streamlit app name
     - Your app URL

2. **Provide Information**
   ```
   Subject: Custom Domain Setup Request
   
   Hello Snowflake Support,
   
   I would like to set up a custom domain for my Streamlit app.
   
   Domain: yourdomain.com
   Snowflake Account: your-account
   Streamlit App: TweeterBot
   Current URL: https://your-account.snowflakecomputing.com/app/TweeterBot
   
   Please let me know what additional configuration is needed.
   
   Thank you,
   [Your Name]
   ```

### Step 4: Alternative Method - Cloudflare (Recommended)

If Snowflake doesn't support direct custom domains, use Cloudflare as a proxy:

1. **Sign up for Cloudflare**
   - Go to [https://cloudflare.com](https://cloudflare.com)
   - Create a free account

2. **Add Your Domain**
   - Click **"Add a Site"**
   - Enter your domain name
   - Select **"Free"** plan

3. **Update Nameservers in GoDaddy**
   - Cloudflare will provide nameservers
   - In GoDaddy, go to **"Nameservers"**
   - Change to **"Custom"**
   - Enter Cloudflare nameservers

4. **Configure DNS in Cloudflare**
   - Go to **"DNS"** → **"Records"**
   - Add CNAME record:
     ```
     Type: CNAME
     Name: @
     Target: your-account.snowflakecomputing.com
     Proxy status: Proxied (orange cloud)
     ```

5. **Set up Page Rules**
   - Go to **"Rules"** → **"Page Rules"**
   - Create rule:
     ```
     URL: yourdomain.com/*
     Settings: Forwarding URL (301 redirect)
     Destination: https://your-account.snowflakecomputing.com/app/TweeterBot
     ```

### Step 5: SSL Certificate Setup

1. **Enable SSL in Cloudflare**
   - Go to **"SSL/TLS"** → **"Overview"**
   - Set encryption mode to **"Full"**

2. **Force HTTPS**
   - Go to **"SSL/TLS"** → **"Edge Certificates"**
   - Enable **"Always Use HTTPS"**

### Step 6: Test Your Domain

1. **Wait for DNS Propagation**
   - DNS changes can take 24-48 hours
   - Use [https://dnschecker.org](https://dnschecker.org) to check

2. **Test Domain Access**
   - Visit your domain: `https://yourdomain.com`
   - Should redirect to your Snowflake app
   - Test image upload and tweet generation

## 🔧 Alternative: Reverse Proxy Setup

If the above methods don't work, set up a reverse proxy:

### Using Nginx (VPS Required)

1. **Get a VPS**
   - Use services like DigitalOcean, Linode, or AWS EC2
   - Install Ubuntu/CentOS

2. **Install Nginx**
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

3. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       
       location / {
           proxy_pass https://your-account.snowflakecomputing.com/app/TweeterBot;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. **Set up SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

## 📊 Domain Configuration Checklist

### GoDaddy DNS Settings
- [ ] CNAME record pointing to Snowflake
- [ ] TTL set to 600 seconds
- [ ] Both @ and www records configured

### Cloudflare Settings (if using)
- [ ] Domain added to Cloudflare
- [ ] Nameservers updated in GoDaddy
- [ ] CNAME record configured
- [ ] Page rule for redirect set up
- [ ] SSL certificate enabled
- [ ] HTTPS redirect enabled

### Testing Checklist
- [ ] Domain resolves to correct IP
- [ ] HTTPS works (no mixed content warnings)
- [ ] Redirect to Snowflake app works
- [ ] App functionality works through domain
- [ ] Mobile access works
- [ ] All features work (image upload, AI generation, etc.)

## 🚨 Troubleshooting

### Common Issues

1. **Domain Not Resolving**
   - Check DNS propagation: [https://dnschecker.org](https://dnschecker.org)
   - Verify CNAME record is correct
   - Wait 24-48 hours for full propagation

2. **SSL Certificate Issues**
   - Ensure HTTPS is enabled
   - Check certificate validity
   - Clear browser cache

3. **Redirect Not Working**
   - Verify page rules in Cloudflare
   - Check Nginx configuration
   - Test with curl: `curl -I https://yourdomain.com`

4. **App Not Loading**
   - Check if Snowflake app is accessible directly
   - Verify proxy configuration
   - Check browser console for errors

### Debug Commands

```bash
# Check DNS resolution
nslookup yourdomain.com

# Check HTTPS
curl -I https://yourdomain.com

# Check redirect
curl -L https://yourdomain.com
```

## 💰 Cost Breakdown

### GoDaddy Domain
- **Domain Registration**: ~$10-15/year
- **DNS Management**: Free

### Cloudflare (Optional)
- **Free Plan**: $0/month
- **Pro Plan**: $20/month (if needed)

### VPS (Alternative)
- **DigitalOcean**: $5-10/month
- **Linode**: $5-10/month
- **AWS EC2**: $5-15/month

## 🎯 Next Steps After Setup

1. **Test Thoroughly**: Verify all functionality works
2. **Update Documentation**: Update any links to use new domain
3. **Monitor Performance**: Check loading times and uptime
4. **Set up Monitoring**: Use services like UptimeRobot
5. **Backup Configuration**: Save DNS and proxy settings

## 📞 Support Resources

### GoDaddy Support
- **Phone**: 1-480-505-8877
- **Live Chat**: Available on GoDaddy website
- **Help Center**: [https://www.godaddy.com/help](https://www.godaddy.com/help)

### Cloudflare Support
- **Community Forum**: [https://community.cloudflare.com](https://community.cloudflare.com)
- **Documentation**: [https://developers.cloudflare.com](https://developers.cloudflare.com)

### Snowflake Support
- **Email**: support@snowflake.com
- **Documentation**: [https://docs.snowflake.com](https://docs.snowflake.com)

---

**🎉 Congratulations!** Once configured, your TweeterBot will be accessible at your custom domain!

**Share your new domain with users: `https://yourdomain.com`** 🚀
