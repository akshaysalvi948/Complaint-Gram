# 🔧 GoDaddy DNS Fix for raiseyourvoice.co.in

## ❌ The Problem
GoDaddy doesn't allow CNAME records for the root domain (@) because it conflicts with other DNS records like MX records.

## ✅ The Solution

### Method 1: Use A Records (GoDaddy Compatible)

#### Step 1: Add A Records for Root Domain
In GoDaddy DNS Management, add these **A records**:

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
```

#### Step 2: Add CNAME for www Subdomain
```
Record 4:
Type: CNAME
Name: www
Value: GMOFVVK-QA77419.snowflakecomputing.com
TTL: 1 Hour
```

### Method 2: Use Cloudflare (Recommended)

Since GoDaddy has limitations, we recommend using Cloudflare:

#### Step 1: Add Domain to Cloudflare
1. Go to [https://cloudflare.com](https://cloudflare.com)
2. Sign up for free account
3. Click "Add a Site"
4. Enter: `raiseyourvoice.co.in`
5. Select "Free" plan

#### Step 2: Update Nameservers in GoDaddy
1. Cloudflare will give you nameservers
2. In GoDaddy, go to "Nameservers"
3. Change to "Custom"
4. Enter Cloudflare nameservers

#### Step 3: Configure DNS in Cloudflare
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

## 🎯 Why Cloudflare is Better

### GoDaddy Limitations:
- ❌ No CNAME for root domain
- ❌ Limited DNS control
- ❌ No automatic SSL
- ❌ Slower performance

### Cloudflare Benefits:
- ✅ CNAME for root domain works
- ✅ Free SSL certificate
- ✅ Better performance (CDN)
- ✅ More DNS control
- ✅ Works immediately

## 🚀 Quick Fix Steps

### Option A: Fix GoDaddy (5 minutes)
1. Delete the failed CNAME record
2. Add the 3 A records above
3. Add the CNAME for www
4. Wait 24-48 hours for propagation

### Option B: Switch to Cloudflare (15 minutes)
1. Add domain to Cloudflare
2. Update nameservers in GoDaddy
3. Configure DNS in Cloudflare
4. Test immediately

## 🧪 Testing

After setup, test your domain:
```bash
# Test DNS resolution
nslookup raiseyourvoice.co.in

# Test HTTPS
curl -I https://raiseyourvoice.co.in
```

## 🎉 Result

Your domain will work at:
- `https://raiseyourvoice.co.in`
- `https://www.raiseyourvoice.co.in`

Both will redirect to your Snowflake Streamlit app!

---

**Recommendation: Use Cloudflare for better control and performance!** 🌐
