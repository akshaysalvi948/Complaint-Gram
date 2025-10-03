# 🌐 Raise Your Voice - Custom Domain Setup Guide

## Your Domain Details
- **Domain**: raiseyourvoice.co.in
- **Snowflake Account**: GMOFVVK-QA77419
- **App URL**: https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot
- **Custom Domain URL**: https://raiseyourvoice.co.in (after setup)

## 🚀 Quick Setup (Choose Your Method)

### Method 1: GoDaddy DNS (Fixed - 5 minutes)

#### Step 1: Log into GoDaddy
1. Go to [https://dcc.godaddy.com](https://dcc.godaddy.com)
2. Sign in with your GoDaddy account
3. Find `raiseyourvoice.co.in` and click **"DNS"**

#### Step 2: Add DNS Records
**IMPORTANT**: GoDaddy doesn't allow CNAME for root domain (@). Use A records instead:

```
Record 1:
Type: A
Name: @
Value: 13.228.155.161
TTL: 1 Hour

Record 2:
Type: A
Name: @
Value: 54.179.32.193
TTL: 1 Hour

Record 3:
Type: A
Name: @
Value: 18.142.35.241
TTL: 1 Hour

Record 4:
Type: CNAME
Name: www
Value: GMOFVVK-QA77419.snowflakecomputing.com
TTL: 1 Hour
```

#### Step 3: Wait and Test
- Wait 24-48 hours for DNS propagation
- Test: `https://raiseyourvoice.co.in`
- Should redirect to your Snowflake app

---

### Method 2: Cloudflare (Recommended - 15 minutes)

#### Step 1: Set up Cloudflare
1. Go to [https://cloudflare.com](https://cloudflare.com)
2. Sign up for **free account**
3. Click **"Add a Site"**
4. Enter: `raiseyourvoice.co.in`
5. Select **"Free"** plan

#### Step 2: Update Nameservers in GoDaddy
1. Cloudflare will give you nameservers like:
   - `ns1.cloudflare.com`
   - `ns2.cloudflare.com`
2. In GoDaddy, go to **"Nameservers"**
3. Change to **"Custom"**
4. Enter Cloudflare nameservers

#### Step 3: Configure DNS in Cloudflare
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

#### Step 4: Set up Redirects
Go to **"Rules"** → **"Page Rules"**:

```
Rule 1:
URL: raiseyourvoice.co.in/*
Setting: Forwarding URL (301)
Destination: https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot

Rule 2:
URL: www.raiseyourvoice.co.in/*
Setting: Forwarding URL (301)
Destination: https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot
```

#### Step 5: Enable SSL
1. Go to **"SSL/TLS"** → **"Overview"**
2. Set encryption to **"Full"**
3. Go to **"SSL/TLS"** → **"Edge Certificates"**
4. Enable **"Always Use HTTPS"**

---

## 🧪 Testing Your Domain

### Quick Tests
```bash
# Test DNS resolution
nslookup raiseyourvoice.co.in

# Test HTTPS
curl -I https://raiseyourvoice.co.in

# Test redirect
curl -L https://raiseyourvoice.co.in
```

### Browser Tests
1. Open `https://raiseyourvoice.co.in`
2. Upload an image
3. Generate a tweet
4. Verify all features work

---

## 🎯 Recommended: Cloudflare Method

**Why Cloudflare?**
- ✅ Free SSL certificate
- ✅ Faster loading times
- ✅ Better security
- ✅ Easy DNS management
- ✅ Works immediately

**Steps:**
1. Add `raiseyourvoice.co.in` to Cloudflare
2. Update nameservers in GoDaddy
3. Configure DNS records
4. Set up redirects
5. Enable SSL
6. Test your domain!

---

## 📋 Step-by-Step Cloudflare Setup

### Step 1: Add Domain to Cloudflare
1. Go to [https://cloudflare.com](https://cloudflare.com)
2. Sign up for free account
3. Click **"Add a Site"**
4. Enter: `raiseyourvoice.co.in`
5. Select **"Free"** plan

### Step 2: Update Nameservers in GoDaddy
1. Cloudflare will show you nameservers like:
   - `ns1.cloudflare.com`
   - `ns2.cloudflare.com`
2. In GoDaddy, go to **"Nameservers"**
3. Change to **"Custom"**
4. Enter the Cloudflare nameservers

### Step 3: Configure DNS Records
In Cloudflare, go to **"DNS"** → **"Records"** and add:

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
Go to **"Rules"** → **"Page Rules"** and add:

```
Rule 1:
URL: raiseyourvoice.co.in/*
Setting: Forwarding URL (301)
Destination: https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot

Rule 2:
URL: www.raiseyourvoice.co.in/*
Setting: Forwarding URL (301)
Destination: https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot
```

### Step 5: Enable SSL
1. Go to **"SSL/TLS"** → **"Overview"**
2. Set encryption to **"Full"**
3. Go to **"SSL/TLS"** → **"Edge Certificates"**
4. Enable **"Always Use HTTPS"**

---

## 🆘 Troubleshooting

### Common Issues
- **Domain not resolving**: Wait 24-48 hours for DNS propagation
- **SSL errors**: Check Cloudflare SSL settings
- **App not loading**: Verify redirects are set up correctly

### Check DNS Propagation
Use [https://dnschecker.org](https://dnschecker.org) to see if `raiseyourvoice.co.in` is resolving globally.

### Test Commands
```bash
# Test DNS resolution
nslookup raiseyourvoice.co.in

# Test HTTPS
curl -I https://raiseyourvoice.co.in

# Test redirect
curl -L https://raiseyourvoice.co.in
```

---

## 🎉 Success!

Once configured, your TweeterBot will be available at:
**`https://raiseyourvoice.co.in`**

Users can access your AI-powered image-to-tweet generator from your custom domain! 🚀

## 📞 Support

If you need help:
1. Check the troubleshooting section above
2. Use the test commands to diagnose issues
3. Contact GoDaddy support for DNS issues
4. Contact Cloudflare support for proxy issues

---

**Ready to set up your domain? Choose Cloudflare method for the best results!** 🌐
