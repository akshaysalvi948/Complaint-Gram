
-- Create TweeterBot Analytics Table
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

-- Grant permissions for public access
GRANT SELECT, INSERT ON TABLE TWEETERBOT_ANALYTICS TO PUBLIC;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_tweeterbot_session ON TWEETERBOT_ANALYTICS(session_id);
CREATE INDEX IF NOT EXISTS idx_tweeterbot_timestamp ON TWEETERBOT_ANALYTICS(timestamp);
CREATE INDEX IF NOT EXISTS idx_tweeterbot_action ON TWEETERBOT_ANALYTICS(action_type);
