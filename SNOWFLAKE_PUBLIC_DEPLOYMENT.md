# 🚀 Deploy TweeterBot to Snowflake Streamlit (Public Access)

This guide will help you deploy your TweeterBot application to Snowflake Streamlit so it's publicly accessible to all users.

## 📋 Prerequisites

### 1. Snowflake Account Setup
- ✅ **Snowflake Account**: You need a Snowflake account with Streamlit Apps enabled
- ✅ **Admin Access**: Account admin privileges to create apps and manage permissions
- ✅ **Compute Resources**: Access to compute resources for running the app

### 2. API Keys Required
- ✅ **Perplexity AI API Key**: For high-quality image descriptions
- ✅ **Hugging Face API Key** (Optional): For free alternative
- ✅ **OpenAI API Key** (Optional): For premium alternative
- ✅ **Twitter API Keys** (Optional): For posting tweets

## 🛠️ Step-by-Step Deployment

### Step 1: Prepare Your Snowflake Environment

1. **Log into Snowflake Web Interface**
   - Go to [https://app.snowflake.com](https://app.snowflake.com)
   - Log in with your admin credentials

2. **Navigate to Streamlit Apps**
   - Click on "Apps" in the left sidebar
   - Select "Streamlit Apps"
   - Click "Create App"

### Step 2: Create the Streamlit App

1. **App Configuration**
   ```
   App Name: TweeterBot
   Description: AI-powered image-to-tweet generator with multiple AI providers
   Version: 1.0
   ```

2. **Upload Your Code**
   - Upload the `app.py` file as `streamlit_app.py`
   - Upload `requirements.txt`
   - Upload `.env.example` as `.env`

### Step 3: Configure Environment Variables

1. **Set up API Keys in Snowflake**
   - Go to "Admin" → "Secrets"
   - Create the following secrets:

   ```sql
   -- Perplexity AI (Required)
   CREATE SECRET perplexity_api_key TYPE = GENERIC_STRING SECRET_STRING = 'your_perplexity_api_key_here';
   
   -- Hugging Face (Optional)
   CREATE SECRET huggingface_api_key TYPE = GENERIC_STRING SECRET_STRING = 'your_huggingface_api_key_here';
   
   -- OpenAI (Optional)
   CREATE SECRET openai_api_key TYPE = GENERIC_STRING SECRET_STRING = 'your_openai_api_key_here';
   
   -- Twitter API (Optional)
   CREATE SECRET twitter_api_key TYPE = GENERIC_STRING SECRET_STRING = 'your_twitter_api_key_here';
   CREATE SECRET twitter_api_secret TYPE = GENERIC_STRING SECRET_STRING = 'your_twitter_api_secret_here';
   CREATE SECRET twitter_access_token TYPE = GENERIC_STRING SECRET_STRING = 'your_twitter_access_token_here';
   CREATE SECRET twitter_access_token_secret TYPE = GENERIC_STRING SECRET_STRING = 'your_twitter_access_token_secret_here';
   ```

### Step 4: Configure Public Access

1. **Set App Permissions**
   ```sql
   -- Grant public access to the app
   GRANT USAGE ON APP TweeterBot TO PUBLIC;
   GRANT USAGE ON DATABASE YOUR_DATABASE TO PUBLIC;
   GRANT USAGE ON SCHEMA YOUR_SCHEMA TO PUBLIC;
   ```

2. **Configure App Settings**
   - Go to your app settings
   - Enable "Public Access"
   - Set appropriate compute size (X-Small recommended for start)

### Step 5: Create Analytics Table

1. **Run this SQL in Snowflake**
   ```sql
   -- Create the analytics table
   CREATE TABLE IF NOT EXISTS TWEETERBOT_ANALYTICS (
       session_id STRING,
       action_type STRING,
       timestamp TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP(),
       image_name STRING,
       image_size INTEGER,
       ai_provider STRING,
       tweet_content STRING,
       success BOOLEAN,
       error_message STRING,
       user_agent STRING,
       ip_address STRING
   );
   
   -- Grant permissions
   GRANT SELECT, INSERT ON TABLE TWEETERBOT_ANALYTICS TO PUBLIC;
   ```

### Step 6: Deploy and Test

1. **Deploy the App**
   - Click "Deploy" in the Streamlit Apps interface
   - Wait for deployment to complete (usually 2-5 minutes)

2. **Test the App**
   - Open the app URL provided by Snowflake
   - Upload a test image
   - Verify AI description generation works
   - Check analytics data is being stored

## 🌐 Making It Publicly Accessible

### Option 1: Direct Snowflake URL
- Snowflake provides a public URL for your app
- Format: `https://your-account.snowflakecomputing.com/app/TweeterBot`
- Share this URL with users

### Option 2: Custom Domain (Advanced)
1. **Purchase a Domain**
   - Buy a domain from any registrar
   - Point it to your Snowflake app

2. **Configure DNS**
   ```
   Type: CNAME
   Name: tweeterbot (or your choice)
   Value: your-account.snowflakecomputing.com
   ```

## 🔧 Configuration Files

### 1. streamlit_app.py
Your main app file (rename from `app.py`)

### 2. requirements.txt
```
streamlit
requests
Pillow
pandas
```

### 3. .env (for local testing)
```bash
# Perplexity AI API Configuration
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# Hugging Face API Configuration (Optional)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# OpenAI API Configuration (Optional)
OPENAI_API_KEY=your_openai_api_key_here

# Twitter API Configuration (Optional)
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here
```

## 📊 Monitoring and Analytics

### 1. View Usage Analytics
```sql
-- Check app usage
SELECT 
    action_type,
    COUNT(*) as usage_count,
    DATE(timestamp) as date
FROM TWEETERBOT_ANALYTICS 
GROUP BY action_type, DATE(timestamp)
ORDER BY date DESC;
```

### 2. Monitor Performance
```sql
-- Check success rates
SELECT 
    ai_provider,
    COUNT(*) as total_requests,
    SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful_requests,
    ROUND(SUM(CASE WHEN success THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate
FROM TWEETERBOT_ANALYTICS 
WHERE action_type = 'ai_generation'
GROUP BY ai_provider;
```

## 🔒 Security Considerations

### 1. API Key Security
- ✅ Store all API keys as Snowflake secrets
- ✅ Never hardcode keys in the app code
- ✅ Use least privilege principle for API access

### 2. Rate Limiting
- ✅ Implement rate limiting for public access
- ✅ Monitor usage patterns
- ✅ Set up alerts for unusual activity

### 3. Data Privacy
- ✅ Don't store sensitive user data
- ✅ Implement proper data retention policies
- ✅ Comply with privacy regulations

## 💰 Cost Management

### 1. Snowflake Costs
- **Compute**: Pay per second of usage
- **Storage**: Pay for data stored
- **Data Transfer**: Pay for data egress

### 2. API Costs
- **Perplexity AI**: ~$0.20 per 1K tokens
- **OpenAI**: ~$0.01-0.03 per 1K tokens
- **Hugging Face**: Free tier available

### 3. Cost Optimization
- Use X-Small compute for low traffic
- Implement caching for repeated requests
- Monitor usage and optimize accordingly

## 🚨 Troubleshooting

### Common Issues

1. **App Won't Start**
   - Check requirements.txt is correct
   - Verify all imports are available
   - Check compute resources

2. **API Keys Not Working**
   - Verify secrets are created correctly
   - Check secret names match code
   - Test API keys independently

3. **Database Errors**
   - Verify table exists
   - Check permissions
   - Test connection

4. **Performance Issues**
   - Increase compute size
   - Optimize code
   - Check for memory leaks

## 📈 Scaling for High Traffic

### 1. Compute Scaling
- Start with X-Small
- Scale up based on usage
- Consider auto-scaling

### 2. Caching
- Implement Redis caching
- Cache API responses
- Cache image processing

### 3. Load Balancing
- Use multiple app instances
- Implement health checks
- Monitor performance

## 🎯 Next Steps

1. **Deploy the App** following the steps above
2. **Test Thoroughly** with various images
3. **Monitor Usage** and performance
4. **Gather Feedback** from users
5. **Iterate and Improve** based on usage patterns

## 📞 Support

If you encounter issues:
1. Check Snowflake documentation
2. Review app logs
3. Test components individually
4. Contact Snowflake support if needed

---

**🎉 Congratulations!** Your TweeterBot is now publicly accessible on Snowflake Streamlit!
