"""
Snowflake Database Manager for TweeterBot
Handles all database operations for storing images, AI-generated content, and analytics
"""

import snowflake.connector
import pandas as pd
import streamlit as st
import uuid
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
import base64
import hashlib

class SnowflakeManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def get_connection_params(self) -> Dict[str, str]:
        """Get Snowflake connection parameters from secrets or environment"""
        try:
            # Try Streamlit secrets first
            return {
                'account': st.secrets.get("snowflake", {}).get("account", ""),
                'user': st.secrets.get("snowflake", {}).get("user", ""),
                'password': st.secrets.get("snowflake", {}).get("password", ""),
                'warehouse': st.secrets.get("snowflake", {}).get("warehouse", ""),
                'database': st.secrets.get("snowflake", {}).get("database", "TWEETERBOT_DB"),
                'schema': st.secrets.get("snowflake", {}).get("schema", "TWEET_DATA"),
                'role': st.secrets.get("snowflake", {}).get("role", "")
            }
        except:
            # Fallback to environment variables
            import os
            return {
                'account': os.getenv('SNOWFLAKE_ACCOUNT', ''),
                'user': os.getenv('SNOWFLAKE_USER', ''),
                'password': os.getenv('SNOWFLAKE_PASSWORD', ''),
                'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', ''),
                'database': os.getenv('SNOWFLAKE_DATABASE', 'TWEETERBOT_DB'),
                'schema': os.getenv('SNOWFLAKE_SCHEMA', 'TWEET_DATA'),
                'role': os.getenv('SNOWFLAKE_ROLE', '')
            }
    
    def connect(self) -> bool:
        """Establish connection to Snowflake"""
        try:
            params = self.get_connection_params()
            
            # Check if required parameters are provided
            if not all([params['account'], params['user'], params['password']]):
                return False
            
            # Remove empty role if not provided
            if not params['role']:
                del params['role']
                
            self.connection = snowflake.connector.connect(**params)
            self.cursor = self.connection.cursor()
            
            # Set database and schema
            self.cursor.execute(f"USE DATABASE {params['database']}")
            self.cursor.execute(f"USE SCHEMA {params['schema']}")
            
            return True
            
        except Exception as e:
            st.error(f"Failed to connect to Snowflake: {str(e)}")
            return False
    
    def disconnect(self):
        """Close Snowflake connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except:
            pass
    
    def is_connected(self) -> bool:
        """Check if connected to Snowflake"""
        return self.connection is not None and not self.connection.is_closed()
    
    def generate_session_id(self, user_ip: str = "", user_agent: str = "") -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        data = f"{user_ip}_{user_agent}_{timestamp}_{uuid.uuid4()}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def create_user_session(self, user_ip: str = "", user_agent: str = "") -> str:
        """Create a new user session"""
        if not self.is_connected():
            return ""
            
        try:
            session_id = self.generate_session_id(user_ip, user_agent)
            
            query = """
            INSERT INTO user_sessions (session_id, user_ip, user_agent)
            VALUES (%s, %s, %s)
            """
            
            self.cursor.execute(query, (session_id, user_ip, user_agent))
            self.connection.commit()
            
            return session_id
            
        except Exception as e:
            st.error(f"Failed to create user session: {str(e)}")
            return ""
    
    def store_uploaded_image(self, session_id: str, image_data: bytes, 
                           filename: str, image_format: str, 
                           width: int, height: int) -> str:
        """Store uploaded image data"""
        if not self.is_connected():
            return ""
            
        try:
            image_id = str(uuid.uuid4())
            
            # Convert image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            query = """
            INSERT INTO uploaded_images 
            (image_id, session_id, original_filename, file_size_bytes, 
             image_format, image_width, image_height, image_data_base64)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(query, (
                image_id, session_id, filename, len(image_data),
                image_format, width, height, image_base64
            ))
            self.connection.commit()
            
            return image_id
            
        except Exception as e:
            st.error(f"Failed to store image: {str(e)}")
            return ""
    
    def store_ai_generated_content(self, image_id: str, ai_provider: str,
                                 generated_text: str, processing_time_ms: int,
                                 api_cost_estimate: float = 0.0) -> str:
        """Store AI-generated content"""
        if not self.is_connected():
            return ""
            
        try:
            content_id = str(uuid.uuid4())
            character_count = len(generated_text)
            
            query = """
            INSERT INTO ai_generated_content 
            (content_id, image_id, ai_provider, generated_text, 
             character_count, processing_time_ms, api_cost_estimate)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(query, (
                content_id, image_id, ai_provider, generated_text,
                character_count, processing_time_ms, api_cost_estimate
            ))
            self.connection.commit()
            
            return content_id
            
        except Exception as e:
            st.error(f"Failed to store AI content: {str(e)}")
            return ""
    
    def store_posted_tweet(self, content_id: str, twitter_tweet_id: str,
                          tweet_text: str, post_success: bool,
                          error_message: str = "") -> str:
        """Store posted tweet information"""
        if not self.is_connected():
            return ""
            
        try:
            tweet_record_id = str(uuid.uuid4())
            
            query = """
            INSERT INTO posted_tweets 
            (tweet_record_id, content_id, twitter_tweet_id, tweet_text, 
             post_success, error_message)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(query, (
                tweet_record_id, content_id, twitter_tweet_id, tweet_text,
                post_success, error_message
            ))
            self.connection.commit()
            
            return tweet_record_id
            
        except Exception as e:
            st.error(f"Failed to store tweet record: {str(e)}")
            return ""
    
    def log_analytics_event(self, session_id: str, event_type: str,
                           ai_provider: str = "", success: bool = True,
                           error_type: str = "", processing_time_ms: int = 0):
        """Log analytics event"""
        if not self.is_connected():
            return
            
        try:
            analytics_id = str(uuid.uuid4())
            
            query = """
            INSERT INTO usage_analytics 
            (analytics_id, session_id, event_type, ai_provider, 
             success, error_type, processing_time_ms)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(query, (
                analytics_id, session_id, event_type, ai_provider,
                success, error_type, processing_time_ms
            ))
            self.connection.commit()
            
        except Exception as e:
            st.error(f"Failed to log analytics: {str(e)}")
    
    def get_daily_usage_stats(self, days: int = 30) -> pd.DataFrame:
        """Get daily usage statistics"""
        if not self.is_connected():
            return pd.DataFrame()
            
        try:
            query = f"""
            SELECT * FROM daily_usage_stats 
            WHERE usage_date >= DATEADD(day, -{days}, CURRENT_DATE())
            ORDER BY usage_date DESC
            """
            
            return pd.read_sql(query, self.connection)
            
        except Exception as e:
            st.error(f"Failed to get usage stats: {str(e)}")
            return pd.DataFrame()
    
    def get_ai_provider_performance(self) -> pd.DataFrame:
        """Get AI provider performance metrics"""
        if not self.is_connected():
            return pd.DataFrame()
            
        try:
            query = "SELECT * FROM ai_provider_performance ORDER BY total_requests DESC"
            return pd.read_sql(query, self.connection)
            
        except Exception as e:
            st.error(f"Failed to get AI performance: {str(e)}")
            return pd.DataFrame()
    
    def get_recent_content(self, limit: int = 50) -> pd.DataFrame:
        """Get recent generated content"""
        if not self.is_connected():
            return pd.DataFrame()
            
        try:
            query = f"""
            SELECT * FROM popular_content 
            ORDER BY generation_timestamp DESC 
            LIMIT {limit}
            """
            
            return pd.read_sql(query, self.connection)
            
        except Exception as e:
            st.error(f"Failed to get recent content: {str(e)}")
            return pd.DataFrame()
    
    def get_user_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for a specific user session"""
        if not self.is_connected():
            return {}
            
        try:
            query = """
            SELECT 
                COUNT(CASE WHEN event_type = 'image_upload' THEN 1 END) as images_uploaded,
                COUNT(CASE WHEN event_type = 'ai_generation' THEN 1 END) as ai_generations,
                COUNT(CASE WHEN event_type = 'tweet_post' THEN 1 END) as tweets_posted,
                AVG(CASE WHEN event_type = 'ai_generation' THEN processing_time_ms END) as avg_ai_time_ms
            FROM usage_analytics 
            WHERE session_id = %s
            """
            
            self.cursor.execute(query, (session_id,))
            result = self.cursor.fetchone()
            
            if result:
                return {
                    'images_uploaded': result[0] or 0,
                    'ai_generations': result[1] or 0,
                    'tweets_posted': result[2] or 0,
                    'avg_ai_time_ms': result[3] or 0
                }
            
            return {}
            
        except Exception as e:
            st.error(f"Failed to get session stats: {str(e)}")
            return {}

# Global instance
snowflake_manager = SnowflakeManager()
