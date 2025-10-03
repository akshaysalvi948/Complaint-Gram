# 🏔️ Snowflake Streamlit in Snowflake (SiS) Deployment Guide

This guide will help you deploy the TweeterBot application directly in Snowflake using Streamlit in Snowflake (SiS).

## 🎯 Overview

The `app_snowflake_sis.py` version has been specifically optimized for Snowflake SiS with the following changes:

### ✅ **What's Included**
- **Direct Twitter API calls** (no tweepy dependency)
- **Native Snowflake connection** (no snowflake-connector-python needed)
- **Streamlit secrets only** (no python-dotenv dependency)
- **Built-in charts** (no plotly dependency)
- **OAuth 1.0a implementation** for Twitter API
- **Simplified analytics** using Snowflake's native capabilities

### ❌ **Removed Dependencies**
- `tweepy` → Replaced with direct HTTP requests
- `python-dotenv` → Using only Streamlit secrets
- `snowflake-connector-python` → Using native SiS connection
- `plotly` → Using Streamlit's built-in charts

## 🚀 Step-by-Step Deployment

### 1. **Prepare Your Snowflake Environment**

```sql
-- Create database and schema
CREATE DATABASE IF NOT EXISTS TWEETERBOT_DB;
USE DATABASE TWEETERBOT_DB;
CREATE SCHEMA IF NOT EXISTS TWEET_DATA;
USE SCHEMA TWEET_DATA;

-- Create analytics table
CREATE TABLE IF NOT EXISTS TWEETERBOT_ANALYTICS (
    session_id VARCHAR(255),
    action_type VARCHAR(100),
    timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    image_name VARCHAR(255),
    image_size INT,
    ai_provider VARCHAR(100),
    generated_text VARCHAR(10000),
    processing_time_ms INT,
    tweet_id VARCHAR(255),
    tweet_text VARCHAR(280),
    success BOOLEAN
);
```

### 2. **Create Secrets (Option A: Snowflake Secrets)**

```sql
-- Create secrets for Twitter API
CREATE SECRET twitter_api_key
TYPE = GENERIC_STRING
SECRET_STRING = 'your_twitter_api_key';

CREATE SECRET twitter_api_secret
TYPE = GENERIC_STRING
SECRET_STRING = 'your_twitter_api_secret';

CREATE SECRET twitter_access_token
TYPE = GENERIC_STRING
SECRET_STRING = 'your_access_token';

CREATE SECRET twitter_access_token_secret
TYPE = GENERIC_STRING
SECRET_STRING = 'your_access_token_secret';

-- Create secrets for AI APIs
CREATE SECRET perplexity_api_key
TYPE = GENERIC_STRING
SECRET_STRING = 'your_perplexity_key';

CREATE SECRET openai_api_key
TYPE = GENERIC_STRING
SECRET_STRING = 'your_openai_key';

CREATE SECRET huggingface_token
TYPE = GENERIC_STRING
SECRET_STRING = 'your_hf_token';
```

### 3. **Create Secrets (Option B: secrets.toml)**

Create a `secrets.toml` file in your Streamlit app directory:

```toml
[twitter]
api_key = "your_twitter_api_key"
api_secret = "your_twitter_api_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

[ai]
perplexity_api_key = "your_perplexity_key"
openai_api_key = "your_openai_key"
huggingface_token = "your_hf_token"
```

### 4. **Upload Files to Snowflake**

1. **Upload the main application file:**
   - Upload `app_snowflake_sis.py` to your Snowflake stage
   - Rename it to `streamlit_app.py` (required by SiS)

2. **Upload requirements:**
   - Upload `requirements_snowflake_sis.txt` as `requirements.txt`

3. **Upload secrets (if using Option B):**
   - Upload `secrets.toml` to the same directory

### 5. **Create Streamlit App in Snowflake**

```sql
-- Create the Streamlit app
CREATE STREAMLIT TWEETERBOT_APP
ROOT_LOCATION = '@your_stage_name'
MAIN_FILE = 'streamlit_app.py'
QUERY_WAREHOUSE = 'your_warehouse_name';

-- Grant necessary permissions
GRANT USAGE ON STREAMLIT TWEETERBOT_APP TO ROLE your_role;
```

### 6. **Access Your App**

```sql
-- Get the app URL
SHOW STREAMLITS;

-- Or directly access via Snowsight
-- Navigate to: Projects > Streamlit > TWEETERBOT_APP
```

## 🔧 Configuration

### **Twitter API Setup**

1. **Create Twitter Developer Account:**
   - Go to [developer.twitter.com](https://developer.twitter.com)
   - Apply for developer access
   - Create a new app

2. **Get API Keys:**
   - API Key and Secret (Consumer Keys)
   - Access Token and Secret
   - Ensure your app has "Read and Write" permissions

3. **Add to Snowflake:**
   - Use either Snowflake secrets or secrets.toml
   - Follow the examples above

### **AI API Setup**

#### **Perplexity AI (Recommended)**
- Sign up at [perplexity.ai](https://www.perplexity.ai)
- Get API key from Settings > API
- Add to your secrets configuration

#### **OpenAI (Paid)**
- Sign up at [platform.openai.com](https://platform.openai.com)
- Create API key
- Add billing information
- Add to your secrets configuration

#### **Hugging Face (Free)**
- Sign up at [huggingface.co](https://huggingface.co)
- Create access token (optional for higher limits)
- Add to your secrets configuration

## 📊 Features Available in SiS Version

### **✅ Core Features**
- ✅ Image upload and display
- ✅ AI-powered tweet generation (3 providers)
- ✅ Tweet editing and character count
- ✅ Direct Twitter posting (OAuth 1.0a)
- ✅ Native Snowflake data storage
- ✅ Basic analytics dashboard
- ✅ Session tracking
- ✅ Error handling and logging

### **📈 Analytics Features**
- ✅ Daily usage statistics
- ✅ AI provider performance metrics
- ✅ Tweet success rates
- ✅ Session analytics
- ✅ Built-in Streamlit charts

### **🔒 Security Features**
- ✅ Secure credential management
- ✅ OAuth 1.0a implementation
- ✅ Session-based tracking
- ✅ Error logging without exposing secrets

## 🐛 Troubleshooting

### **Common Issues**

#### **1. Import Errors**
```
ModuleNotFoundError: No module named 'tweepy'
```
**Solution:** Make sure you're using `app_snowflake_sis.py` and `requirements_snowflake_sis.txt`

#### **2. Twitter API Errors**
```
Error: 401 - Unauthorized
```
**Solution:** 
- Verify your Twitter API credentials
- Ensure your app has "Read and Write" permissions
- Check that access tokens are not expired

#### **3. Snowflake Connection Issues**
```
Error loading analytics: 'snowflake' connection not found
```
**Solution:**
- Ensure you're running in Snowflake SiS environment
- Verify database and schema exist
- Check table permissions

#### **4. AI API Errors**
```
Error: 429 - Rate limit exceeded
```
**Solution:**
- Wait for rate limit reset
- Consider upgrading API plan
- Switch to different AI provider temporarily

### **Performance Optimization**

1. **Use appropriate warehouse size:**
   ```sql
   ALTER WAREHOUSE your_warehouse SET WAREHOUSE_SIZE = 'SMALL';
   ```

2. **Optimize queries:**
   - Use appropriate date filters
   - Add indexes if needed
   - Limit result sets

3. **Monitor usage:**
   ```sql
   -- Check app usage
   SELECT * FROM TWEETERBOT_ANALYTICS 
   ORDER BY timestamp DESC 
   LIMIT 100;
   ```

## 📝 File Structure

```
your_snowflake_stage/
├── streamlit_app.py          # Main app (renamed from app_snowflake_sis.py)
├── requirements.txt          # SiS compatible requirements
├── secrets.toml             # Secrets configuration (optional)
└── README.md               # This deployment guide
```

## 🎉 Success Checklist

- [ ] Snowflake database and schema created
- [ ] Analytics table created
- [ ] Twitter API credentials configured
- [ ] AI API keys configured
- [ ] Files uploaded to Snowflake stage
- [ ] Streamlit app created in Snowflake
- [ ] App accessible via Snowsight
- [ ] Image upload working
- [ ] AI generation working
- [ ] Twitter posting working
- [ ] Analytics dashboard displaying data

## 🆘 Support

If you encounter issues:

1. **Check Snowflake logs:**
   ```sql
   -- View app logs
   SHOW LOGS FOR STREAMLIT TWEETERBOT_APP;
   ```

2. **Verify permissions:**
   ```sql
   -- Check your role permissions
   SHOW GRANTS TO ROLE your_role;
   ```

3. **Test individual components:**
   - Test AI APIs separately
   - Verify Twitter credentials
   - Check Snowflake connectivity

## 🚀 Next Steps

Once deployed successfully:

1. **Monitor usage** via the analytics dashboard
2. **Optimize performance** based on usage patterns
3. **Scale resources** as needed
4. **Add custom features** specific to your use case
5. **Set up monitoring** and alerting

---

**🎯 Your TweeterBot is now ready to run natively in Snowflake!** 

Enjoy the seamless integration with Snowflake's data platform and the power of AI-driven social media content generation! 🐦✨
