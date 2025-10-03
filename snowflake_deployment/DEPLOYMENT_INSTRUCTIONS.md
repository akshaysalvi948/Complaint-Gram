
# Snowflake Streamlit Deployment Instructions

## Files to Upload to Snowflake:
1. streamlit_app.py (main app file)
2. requirements.txt (dependencies)
3. .env.example (environment variables template)

## Steps:
1. Log into Snowflake Web Interface
2. Go to Apps → Streamlit Apps
3. Click "Create App"
4. Upload the files above
5. Configure environment variables as secrets
6. Deploy the app

## Environment Variables to Set:
- PERPLEXITY_API_KEY (required)
- HUGGINGFACE_API_KEY (optional)
- OPENAI_API_KEY (optional)
- TWITTER_API_KEY (optional)
- TWITTER_API_SECRET (optional)
- TWITTER_ACCESS_TOKEN (optional)
- TWITTER_ACCESS_TOKEN_SECRET (optional)

## SQL to Run in Snowflake:
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

## Public Access:
After deployment, your app will be available at:
https://your-account.snowflakecomputing.com/app/TweeterBot

Share this URL with users for public access.
