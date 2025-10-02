-- Snowflake Database Schema for TweeterBot
-- This script creates the necessary tables to store image and text data

-- Create database and schema
CREATE DATABASE IF NOT EXISTS TWEETERBOT_DB;
USE DATABASE TWEETERBOT_DB;
CREATE SCHEMA IF NOT EXISTS TWEET_DATA;
USE SCHEMA TWEET_DATA;

-- Table to store user sessions and metadata
CREATE OR REPLACE TABLE user_sessions (
    session_id STRING PRIMARY KEY,
    user_ip STRING,
    user_agent STRING,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    last_activity TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Table to store uploaded images
CREATE OR REPLACE TABLE uploaded_images (
    image_id STRING PRIMARY KEY,
    session_id STRING,
    original_filename STRING,
    file_size_bytes NUMBER,
    image_format STRING,
    image_width NUMBER,
    image_height NUMBER,
    image_data_base64 STRING, -- Store base64 encoded image
    upload_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
);

-- Table to store AI-generated content
CREATE OR REPLACE TABLE ai_generated_content (
    content_id STRING PRIMARY KEY,
    image_id STRING,
    ai_provider STRING, -- 'perplexity', 'openai', 'huggingface'
    generated_text STRING,
    character_count NUMBER,
    generation_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    processing_time_ms NUMBER,
    api_cost_estimate NUMBER(10,4), -- Estimated cost in USD
    FOREIGN KEY (image_id) REFERENCES uploaded_images(image_id)
);

-- Table to store tweet posts
CREATE OR REPLACE TABLE posted_tweets (
    tweet_record_id STRING PRIMARY KEY,
    content_id STRING,
    twitter_tweet_id STRING, -- Actual Twitter tweet ID
    tweet_text STRING,
    post_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    post_success BOOLEAN,
    error_message STRING,
    FOREIGN KEY (content_id) REFERENCES ai_generated_content(content_id)
);

-- Table to store analytics and metrics
CREATE OR REPLACE TABLE usage_analytics (
    analytics_id STRING PRIMARY KEY,
    session_id STRING,
    event_type STRING, -- 'image_upload', 'ai_generation', 'tweet_post'
    ai_provider STRING,
    success BOOLEAN,
    error_type STRING,
    processing_time_ms NUMBER,
    timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
);

-- Create views for analytics
CREATE OR REPLACE VIEW daily_usage_stats AS
SELECT 
    DATE(timestamp) as usage_date,
    COUNT(*) as total_events,
    COUNT(CASE WHEN event_type = 'image_upload' THEN 1 END) as image_uploads,
    COUNT(CASE WHEN event_type = 'ai_generation' THEN 1 END) as ai_generations,
    COUNT(CASE WHEN event_type = 'tweet_post' THEN 1 END) as tweet_posts,
    COUNT(CASE WHEN success = TRUE THEN 1 END) as successful_events,
    COUNT(CASE WHEN success = FALSE THEN 1 END) as failed_events
FROM usage_analytics
GROUP BY DATE(timestamp)
ORDER BY usage_date DESC;

CREATE OR REPLACE VIEW ai_provider_performance AS
SELECT 
    ai_provider,
    COUNT(*) as total_requests,
    AVG(processing_time_ms) as avg_processing_time_ms,
    COUNT(CASE WHEN success = TRUE THEN 1 END) as successful_requests,
    COUNT(CASE WHEN success = FALSE THEN 1 END) as failed_requests,
    (successful_requests / total_requests * 100) as success_rate_percent
FROM usage_analytics 
WHERE ai_provider IS NOT NULL
GROUP BY ai_provider;

CREATE OR REPLACE VIEW popular_content AS
SELECT 
    ag.ai_provider,
    ag.generated_text,
    ag.character_count,
    ui.original_filename,
    ag.generation_timestamp,
    CASE WHEN pt.post_success THEN 'Posted' ELSE 'Not Posted' END as post_status
FROM ai_generated_content ag
JOIN uploaded_images ui ON ag.image_id = ui.image_id
LEFT JOIN posted_tweets pt ON ag.content_id = pt.content_id
ORDER BY ag.generation_timestamp DESC;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON user_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_images_upload_timestamp ON uploaded_images(upload_timestamp);
CREATE INDEX IF NOT EXISTS idx_content_generation_timestamp ON ai_generated_content(generation_timestamp);
CREATE INDEX IF NOT EXISTS idx_tweets_post_timestamp ON posted_tweets(post_timestamp);
CREATE INDEX IF NOT EXISTS idx_analytics_timestamp ON usage_analytics(timestamp);
CREATE INDEX IF NOT EXISTS idx_analytics_event_type ON usage_analytics(event_type);

-- Grant permissions (adjust as needed for your setup)
-- GRANT USAGE ON DATABASE TWEETERBOT_DB TO ROLE TWEETERBOT_ROLE;
-- GRANT USAGE ON SCHEMA TWEET_DATA TO ROLE TWEETERBOT_ROLE;
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA TWEET_DATA TO ROLE TWEETERBOT_ROLE;
-- GRANT SELECT ON ALL VIEWS IN SCHEMA TWEET_DATA TO ROLE TWEETERBOT_ROLE;
