# 🚀 Quick Start: Deploy TweeterBot to Snowflake Streamlit

## ⚡ Fast Track Deployment (5 Minutes)

### Step 1: Get Your Snowflake Account Ready
1. **Log into Snowflake**: Go to [https://app.snowflake.com](https://app.snowflake.com)
2. **Navigate to Apps**: Click "Apps" → "Streamlit Apps"
3. **Create New App**: Click "Create App"

### Step 2: Upload Your Files
Upload these files from the `snowflake_deployment` folder:
- ✅ `streamlit_app.py` (main app file)
- ✅ `requirements.txt` (dependencies)

### Step 3: Set Up API Keys
In Snowflake, go to **Admin** → **Secrets** and create:

```sql
-- Required: Perplexity AI
CREATE SECRET perplexity_api_key TYPE = GENERIC_STRING SECRET_STRING = 'your_perplexity_api_key_here';

-- Optional: Hugging Face (free alternative)
CREATE SECRET huggingface_api_key TYPE = GENERIC_STRING SECRET_STRING = 'your_huggingface_api_key_here';

-- Optional: OpenAI (premium alternative)
CREATE SECRET openai_api_key TYPE = GENERIC_STRING SECRET_STRING = 'your_openai_api_key_here';
```

### Step 4: Create Analytics Table
Run this SQL in Snowflake:

```sql
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

GRANT SELECT, INSERT ON TABLE TWEETERBOT_ANALYTICS TO PUBLIC;
```

### Step 5: Deploy and Test
1. **Deploy**: Click "Deploy" in Snowflake
2. **Get URL**: Copy the public URL (e.g., `https://your-account.snowflakecomputing.com/app/TweeterBot`)
3. **Test**: Upload an image and generate a tweet
4. **Share**: Share the URL with users!

## 🌐 Making It Public

### Option 1: Direct Snowflake URL
- Your app gets a public URL automatically
- Format: `https://your-account.snowflakecomputing.com/app/TweeterBot`
- Share this URL with anyone!

### Option 2: Custom Domain (Optional)
1. Buy a domain (e.g., `tweeterbot.com`)
2. Point DNS to your Snowflake app
3. Users can access via your custom domain

## 💰 Cost Estimation

### Snowflake Costs (Approximate)
- **X-Small Compute**: ~$0.0001 per second
- **Storage**: ~$0.023 per GB per month
- **Data Transfer**: ~$0.09 per GB

### API Costs
- **Perplexity AI**: ~$0.20 per 1K tokens
- **Hugging Face**: Free tier available
- **OpenAI**: ~$0.01-0.03 per 1K tokens

### Example Monthly Cost (100 users/day)
- Snowflake: ~$5-10/month
- Perplexity AI: ~$10-20/month
- **Total**: ~$15-30/month

## 🔧 Troubleshooting

### Common Issues
1. **App won't start**: Check requirements.txt
2. **API errors**: Verify secrets are set correctly
3. **Database errors**: Run the SQL setup script
4. **Slow performance**: Increase compute size

### Quick Fixes
- Check app logs in Snowflake
- Verify all secrets are created
- Test API keys independently
- Ensure table exists and has permissions

## 📊 Monitor Usage

### View Analytics
```sql
-- Check daily usage
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as total_requests,
    COUNT(DISTINCT session_id) as unique_users
FROM TWEETERBOT_ANALYTICS 
GROUP BY DATE(timestamp)
ORDER BY date DESC;
```

### Monitor Performance
```sql
-- Check success rates
SELECT 
    ai_provider,
    COUNT(*) as requests,
    SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful,
    ROUND(SUM(CASE WHEN success THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate
FROM TWEETERBOT_ANALYTICS 
GROUP BY ai_provider;
```

## 🎯 Next Steps After Deployment

1. **Test Thoroughly**: Try different image types
2. **Monitor Usage**: Check analytics regularly
3. **Gather Feedback**: Ask users for input
4. **Optimize**: Improve based on usage patterns
5. **Scale**: Increase compute if needed

## 🆘 Need Help?

1. **Check Logs**: Review app logs in Snowflake
2. **Test Components**: Verify each part works
3. **Snowflake Docs**: Check official documentation
4. **Support**: Contact Snowflake support if needed

---

**🎉 That's it!** Your TweeterBot is now publicly accessible on Snowflake Streamlit!

**Share your app URL and let users start generating amazing tweets from their images!** 🚀
