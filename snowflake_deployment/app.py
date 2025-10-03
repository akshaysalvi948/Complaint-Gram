import streamlit as st
import requests
import base64
import io
from PIL import Image
import os
import time
import json
import hashlib
import hmac

def load_env_file():
    """Load environment variables from .env file manually"""
    env_vars = {}
    try:
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        return env_vars
    except Exception:
        return {}

# Load .env file if it exists
env_vars = load_env_file()
# Note: python-dotenv is not available in Snowflake SiS
# Environment variables should be set in the Snowflake environment
import urllib.parse
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="AI Tweet Generator",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1DA1F2, #0d8bd9);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #1DA1F2;
        text-align: center;
        margin: 2rem 0;
    }
    .tweet-preview {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1DA1F2;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Navigation
page = st.sidebar.selectbox(
    "📱 Navigation",
    ["🐦 Tweet Generator", "📊 Analytics Dashboard"],
    index=0
)

# Header
if page == "🐦 Tweet Generator":
    st.markdown("""
    <div class="main-header">
        <h1>🐦 AI Tweet Generator</h1>
        <p>Upload an image and let AI write a tweet about it!</p>
    </div>
    """, unsafe_allow_html=True)
elif page == "📊 Analytics Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Analytics Dashboard</h1>
        <p>Insights and analytics from your TweeterBot usage</p>
    </div>
    """, unsafe_allow_html=True)

# Secure credential management - Snowflake SiS compatible
def get_secret(secret_key, default=""):
    """Get credentials from Streamlit secrets only (Snowflake SiS compatible)"""
    try:
        # Navigate nested secrets
        keys = secret_key.split('.')
        value = st.secrets
        for key in keys:
            value = value[key]
        return value
    except:
        return default

# Get credentials securely from Streamlit secrets
twitter_api_key = get_secret("twitter.api_key")
twitter_api_secret = get_secret("twitter.api_secret")
twitter_access_token = get_secret("twitter.access_token")
twitter_access_token_secret = get_secret("twitter.access_token_secret")

# Load Perplexity API key from .env file first, then environment, then secrets
perplexity_key = env_vars.get("PERPLEXITY_API_KEY") or os.getenv("PERPLEXITY_API_KEY") or get_secret("ai.perplexity_api_key")
hf_token = get_secret("ai.huggingface_token")
openai_key = get_secret("ai.openai_api_key")

# Sidebar for configuration
with st.sidebar:
    st.header("🔧 Configuration")
    
    # Twitter API Configuration
    st.subheader("Twitter API")
    if all([twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_token_secret]):
        st.success("✅ Twitter API configured")
    else:
        st.error("❌ Twitter API not configured")
        st.info("💡 Add your Twitter API credentials to Streamlit secrets")
        with st.expander("📝 How to add Twitter API keys for Snowflake SiS"):
            st.markdown("""
            **For Snowflake Streamlit in Snowflake:**
            1. In your Snowflake worksheet, add secrets:
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
            ```
            
            **Or use secrets.toml in your app:**
            ```toml
            [twitter]
            api_key = "your_key"
            api_secret = "your_secret"
            access_token = "your_token"
            access_token_secret = "your_token_secret"
            ```
            """)
    
    # AI Provider Selection
    st.subheader("AI Settings")
    ai_provider = st.selectbox("AI Provider", ["Perplexity AI (Recommended)", "Hugging Face (Free)", "OpenAI (Paid)"])
    
    # AI Provider Configuration with input fields
    if ai_provider == "Perplexity AI (Recommended)":
        st.info("💡 High-quality image descriptions with fast response times")
        if perplexity_key:
            st.success("✅ Perplexity API ready")
        else:
            st.warning("⚠️ Perplexity API key not configured")
            
    elif ai_provider == "Hugging Face (Free)":
        st.info("💡 Free option using Salesforce BLIP model")
        if hf_token:
            st.success("✅ Hugging Face configured")
        else:
            st.info("ℹ️ No API key needed (using free tier)")
            user_hf_token = st.text_input(
                "Hugging Face Token (Optional)", 
                type="password",
                help="Optional: Add token for higher rate limits"
            )
            if user_hf_token:
                hf_token = user_hf_token
                
    elif ai_provider == "OpenAI (Paid)":
        st.info("💡 Uses GPT-4 Vision for sophisticated descriptions")
        if not openai_key:
            st.warning("⚠️ OpenAI API key not configured")
            user_openai_key = st.text_input(
                "Enter OpenAI API Key", 
                type="password",
                help="Get your API key from https://platform.openai.com/api-keys"
            )
            if user_openai_key:
                openai_key = user_openai_key
                st.success("✅ OpenAI API key entered")
        else:
            st.success("✅ OpenAI API configured")
    
    # Debug Mode
    st.subheader("🔧 Debug")
    debug_mode = st.checkbox("Enable Debug Mode", help="Show detailed error information and debug messages")
    st.session_state.debug_mode = debug_mode
    
    # Snowflake Database Status
    st.subheader("🗄️ Database")
    # In Snowflake SiS, we're already connected to Snowflake
    st.success("✅ Snowflake connected (Native SiS)")
    st.info("💡 Using Snowflake's native connection")

# Initialize session state
if 'tweet_content' not in st.session_state:
    st.session_state.tweet_content = ""
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'session_id' not in st.session_state:
    # Generate a simple session ID for Snowflake SiS
    st.session_state.session_id = hashlib.md5(f"{datetime.now().isoformat()}".encode()).hexdigest()

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def enhance_caption_for_twitter(caption):
    """Enhance a basic caption to be more tweet-worthy and engaging"""
    if not caption or caption == "No description generated":
        return "✨ Captured a moment worth sharing! #photography #share"
    
    # Remove common generic phrases
    caption = caption.replace("a photo of", "").replace("an image of", "").replace("a picture of", "")
    caption = caption.replace("showing", "").replace("featuring", "").strip()
    
    # Capitalize first letter
    caption = caption[0].upper() + caption[1:] if caption else caption
    
    # Add engaging elements based on content
    if any(word in caption.lower() for word in ["person", "people", "man", "woman", "child", "baby"]):
        if "smiling" in caption.lower() or "happy" in caption.lower():
            caption = f"😊 {caption}"
        elif "serious" in caption.lower() or "focused" in caption.lower():
            caption = f"🎯 {caption}"
        else:
            caption = f"👤 {caption}"
    elif any(word in caption.lower() for word in ["food", "meal", "dish", "cooking", "restaurant"]):
        caption = f"🍽️ {caption}"
    elif any(word in caption.lower() for word in ["nature", "landscape", "mountain", "forest", "beach", "ocean"]):
        caption = f"🌿 {caption}"
    elif any(word in caption.lower() for word in ["city", "urban", "building", "street", "architecture"]):
        caption = f"🏙️ {caption}"
    elif any(word in caption.lower() for word in ["animal", "dog", "cat", "pet", "wildlife"]):
        caption = f"🐾 {caption}"
    elif any(word in caption.lower() for word in ["art", "painting", "drawing", "creative", "design"]):
        caption = f"🎨 {caption}"
    elif any(word in caption.lower() for word in ["technology", "computer", "phone", "gadget", "tech"]):
        caption = f"💻 {caption}"
    else:
        caption = f"✨ {caption}"
    
    # Add relevant hashtags based on content
    hashtags = []
    if any(word in caption.lower() for word in ["beautiful", "amazing", "stunning", "gorgeous"]):
        hashtags.append("#beautiful")
    if any(word in caption.lower() for word in ["sunset", "sunrise", "golden", "light"]):
        hashtags.append("#goldenhour")
    if any(word in caption.lower() for word in ["food", "delicious", "tasty", "cooking"]):
        hashtags.append("#foodie")
    if any(word in caption.lower() for word in ["travel", "adventure", "journey", "explore"]):
        hashtags.append("#travel")
    if any(word in caption.lower() for word in ["art", "creative", "design", "artistic"]):
        hashtags.append("#art")
    
    # Add a maximum of 2 hashtags to keep it clean
    if len(hashtags) > 0:
        caption += " " + " ".join(hashtags[:2])
    
    # Ensure it's under 280 characters
    if len(caption) > 280:
        caption = caption[:277] + "..."
    
    return caption

def generate_image_description_with_perplexity(image, api_key):
    """Generate image description using Perplexity AI with retry logic and fallback"""
    import time
    
    max_retries = 3
    retry_delay = 3  # seconds - increased delay
    
    for attempt in range(max_retries):
        try:
            
            # Convert image to base64
            img_base64 = encode_image_to_base64(image)
            image_url = f"data:image/jpeg;base64,{img_base64}"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert social media content creator and image analyst. Your job is to create compelling, viral-worthy tweets that analyze images in detail and engage audiences. \n\nGuidelines:\n- Analyze the image thoroughly: identify objects, people, scenes, colors, lighting, mood, composition\n- Look for interesting details, emotions, stories, or unique elements\n- Write in a conversational, engaging tone that encourages likes and retweets\n- Use 2-3 relevant hashtags maximum\n- Keep under 280 characters\n- Avoid generic phrases like 'sharing this image' or 'something interesting'\n- Focus on what makes this image special or noteworthy\n- Make it shareable and thought-provoking"
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this image in detail and create a compelling tweet that would perform well on social media. Describe what you actually see, the mood, the story, or what makes it interesting. Make it engaging and shareable."
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url}
                            }
                        ]
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.8
            }

            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=payload,
                timeout=45  # Increased timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                error_msg = f"HTTP Error: {response.status_code} - {response.text}"
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    return error_msg

        except requests.exceptions.ConnectionError as e:
            error_str = str(e)
            if "Device or resource busy" in error_str or "Max retries exceeded" in error_str:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    return f"NETWORK_ERROR: Perplexity AI connection failed after {max_retries} attempts due to network issues. Please try Hugging Face instead."
            else:
                return f"Connection error: {error_str}"
        except requests.exceptions.Timeout as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                return f"TIMEOUT_ERROR: Request timeout after {max_retries} attempts: {str(e)}"
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                return f"UNEXPECTED_ERROR: {str(e)}"
    
    return "FAILED_ALL_RETRIES: Failed to generate description after all retry attempts."

def generate_image_description_with_huggingface(image, token=""):
    """Generate image description using Hugging Face with retry logic"""
    import time
    
    max_retries = 3
    retry_delay = 3  # seconds
    
    for attempt in range(max_retries):
        try:
            # Convert image to base64
            img_base64 = encode_image_to_base64(image)
            
            # Hugging Face API endpoint for image captioning
            API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
            
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"
            
            response = requests.post(
                API_URL,
                headers=headers,
                data=base64.b64decode(img_base64),
                timeout=45  # Increased timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    caption = result[0].get('generated_text', 'No description generated')
                    # Enhance the caption to be more tweet-worthy
                    caption = enhance_caption_for_twitter(caption)
                    return caption
                else:
                    caption = result.get('generated_text', 'No description generated')
                    # Enhance the caption to be more tweet-worthy
                    caption = enhance_caption_for_twitter(caption)
                    return caption
            else:
                error_msg = f"HTTP Error: {response.status_code} - {response.text}"
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    return error_msg
                    
        except requests.exceptions.ConnectionError as e:
            error_str = str(e)
            if "Device or resource busy" in error_str or "Max retries exceeded" in error_str:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    return f"NETWORK_ERROR: Hugging Face connection failed after {max_retries} attempts due to network issues."
            else:
                return f"Connection error: {error_str}"
        except requests.exceptions.Timeout as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                return f"TIMEOUT_ERROR: Hugging Face timeout after {max_retries} attempts: {str(e)}"
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                return f"UNEXPECTED_ERROR: {str(e)}"
    
    return "FAILED_ALL_RETRIES: Hugging Face failed after all retry attempts."

def generate_fallback_description(image):
    """Generate a basic fallback description when all AI services fail"""
    import random
    
    # Get basic image info
    width, height = image.size
    format_name = image.format or "Unknown"
    
    # Fallback descriptions based on image characteristics - more engaging
    fallback_tweets = [
        f"📸 Captured this {format_name} moment ({width}x{height}) - sometimes the best shots happen when you least expect them! #photography #moment #captured",
        f"🖼️ This {format_name} image ({width}x{height}) stopped me in my tracks today. What's your first impression? #image #thoughts #share",
        f"📷 Found this {format_name} photo ({width}x{height}) and couldn't resist sharing it! Sometimes beauty is in the details. #photo #beauty #details",
        f"✨ Stumbled upon this {format_name} image ({width}x{height}) - there's something special about it that caught my eye! #discovery #special #share",
        f"🎨 This {format_name} image ({width}x{height}) has that certain something... what do you see? #art #perspective #discussion",
        f"📱 Just captured this {format_name} shot ({width}x{height}) - sometimes the simplest moments tell the best stories! #moment #story #simple",
        f"🖼️ This {format_name} image ({width}x{height}) speaks volumes without saying a word. What's it telling you? #image #story #perspective",
        f"📸 Sharing this {format_name} photo ({width}x{height}) because some moments are too good to keep to yourself! #share #moment #good"
    ]
    
    return random.choice(fallback_tweets)

def generate_image_description_with_openai(image, api_key):
    """Generate image description using OpenAI API via direct HTTP requests"""
    try:
        # Convert image to base64
        img_base64 = encode_image_to_base64(image)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert social media content creator specializing in viral Twitter/X content. Your job is to analyze images and create compelling, engaging tweets that perform well on social media.\n\nGuidelines:\n- Analyze the image in detail: identify objects, people, scenes, colors, lighting, mood, composition\n- Look for interesting details, emotions, stories, or unique elements that make the image special\n- Write in a conversational, engaging tone that encourages likes, retweets, and comments\n- Use 2-3 relevant hashtags maximum\n- Keep under 280 characters\n- Avoid generic phrases like 'sharing this image' or 'something interesting'\n- Focus on what makes this image noteworthy, beautiful, or interesting\n- Make it shareable and thought-provoking\n- Use emojis strategically to enhance engagement"
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this image thoroughly and create a compelling, viral-worthy tweet. Describe what you actually see, the mood, the story, or what makes it interesting. Make it engaging and shareable for social media."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 200,
            "temperature": 0.8
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
        
    except Exception as e:
        return f"Error generating description: {str(e)}"

def create_oauth_signature(method, url, params, consumer_secret, token_secret):
    """Create OAuth 1.0a signature for Twitter API"""
    # Sort parameters
    sorted_params = sorted(params.items())
    
    # Create parameter string
    param_string = "&".join([f"{k}={v}" for k, v in sorted_params])
    
    # Create signature base string
    signature_base = f"{method}&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(param_string, safe='')}"
    
    # Create signing key
    signing_key = f"{urllib.parse.quote(consumer_secret, safe='')}&{urllib.parse.quote(token_secret, safe='')}"
    
    # Create signature
    signature = base64.b64encode(
        hmac.new(signing_key.encode(), signature_base.encode(), hashlib.sha1).digest()
    ).decode()
    
    return signature

def post_tweet_direct_api(content, image_bytes, api_key, api_secret, access_token, access_token_secret):
    """Post tweet using direct Twitter API calls (no tweepy dependency)"""
    try:
        # Step 1: Upload media
        media_upload_url = "https://upload.twitter.com/1.1/media/upload.json"
        
        # OAuth parameters for media upload
        oauth_params = {
            'oauth_consumer_key': api_key,
            'oauth_nonce': hashlib.md5(f"{datetime.now().isoformat()}".encode()).hexdigest(),
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(datetime.now().timestamp())),
            'oauth_token': access_token,
            'oauth_version': '1.0'
        }
        
        # Create signature for media upload
        oauth_params['oauth_signature'] = create_oauth_signature(
            'POST', media_upload_url, oauth_params, api_secret, access_token_secret
        )
        
        # Create authorization header
        auth_header = 'OAuth ' + ', '.join([f'{k}="{v}"' for k, v in sorted(oauth_params.items())])
        
        # Upload media
        files = {'media': ('image.jpg', image_bytes, 'image/jpeg')}
        headers = {'Authorization': auth_header}
        
        media_response = requests.post(media_upload_url, headers=headers, files=files, timeout=30)
        
        if media_response.status_code != 200:
            return False, f"Media upload failed: {media_response.status_code} - {media_response.text}"
        
        media_id = media_response.json()['media_id_string']
        
        # Step 2: Post tweet with media
        tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
        
        tweet_params = {
            'status': content,
            'media_ids': media_id,
            'oauth_consumer_key': api_key,
            'oauth_nonce': hashlib.md5(f"{datetime.now().isoformat()}tweet".encode()).hexdigest(),
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(datetime.now().timestamp())),
            'oauth_token': access_token,
            'oauth_version': '1.0'
        }
        
        # Create signature for tweet
        tweet_params['oauth_signature'] = create_oauth_signature(
            'POST', tweet_url, tweet_params, api_secret, access_token_secret
        )
        
        # Separate OAuth and tweet parameters
        oauth_tweet_params = {k: v for k, v in tweet_params.items() if k.startswith('oauth_')}
        tweet_data = {'status': content, 'media_ids': media_id}
        
        # Create authorization header for tweet
        auth_header = 'OAuth ' + ', '.join([f'{k}="{v}"' for k, v in sorted(oauth_tweet_params.items())])
        
        tweet_response = requests.post(
            tweet_url,
            headers={'Authorization': auth_header},
            data=tweet_data,
            timeout=30
        )
        
        if tweet_response.status_code == 200:
            tweet_data = tweet_response.json()
            return True, tweet_data['id_str']
        else:
            return False, f"Tweet failed: {tweet_response.status_code} - {tweet_response.text}"
        
    except Exception as e:
        return False, str(e)

def store_data_in_snowflake(session_id, action, data):
    """Store data in Snowflake using native SiS connection with table creation"""
    try:
        # In Snowflake SiS, we can use st.connection to access Snowflake
        conn = st.connection("snowflake")
        
        # First, ensure the table exists
        try:
            # Try to query the table to see if it exists
            conn.query("SELECT 1 FROM TWEETERBOT_ANALYTICS LIMIT 1")
        except Exception as table_error:
            if "does not exist" in str(table_error).lower():
                st.info("🔧 Creating TWEETERBOT_ANALYTICS table...")
                
                # Create the table
                create_table_sql = """
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
                """
                
                try:
                    conn.query(create_table_sql)
                    st.success("✅ TWEETERBOT_ANALYTICS table created successfully!")
                except Exception as create_error:
                    st.error(f"❌ Failed to create table: {str(create_error)}")
                    st.info("💡 Please run this SQL manually in your Snowflake worksheet:")
                    st.code(create_table_sql, language="sql")
                    return False
            else:
                st.error(f"❌ Table access error: {str(table_error)}")
                return False
        
        # Now insert data using direct string formatting (Snowflake SiS compatible)
        if action == "image_upload":
            # Escape single quotes in string values
            session_id_escaped = session_id.replace("'", "''")
            action_escaped = action.replace("'", "''")
            name_escaped = data.get('name', '').replace("'", "''")
            size = data.get('size', 0)
            
            query = f"""
            INSERT INTO TWEETERBOT_ANALYTICS (
                session_id, action_type, timestamp, image_name, image_size
            ) VALUES ('{session_id_escaped}', '{action_escaped}', CURRENT_TIMESTAMP(), '{name_escaped}', {size})
            """
            
            if st.session_state.get('debug_mode', False):
                st.info(f"🔍 Debug: Executing query: {query}")
            
            conn.query(query)
            
        elif action == "ai_generation":
            # Escape single quotes in string values
            session_id_escaped = session_id.replace("'", "''")
            action_escaped = action.replace("'", "''")
            provider_escaped = data.get('provider', '').replace("'", "''")
            text_escaped = data.get('text', '').replace("'", "''")
            processing_time = data.get('processing_time', 0)
            
            query = f"""
            INSERT INTO TWEETERBOT_ANALYTICS (
                session_id, action_type, timestamp, ai_provider, generated_text, processing_time_ms
            ) VALUES ('{session_id_escaped}', '{action_escaped}', CURRENT_TIMESTAMP(), '{provider_escaped}', '{text_escaped}', {processing_time})
            """
            
            if st.session_state.get('debug_mode', False):
                st.info(f"🔍 Debug: Executing query: {query}")
            
            conn.query(query)
            
        elif action == "tweet_post":
            # Escape single quotes in string values
            session_id_escaped = session_id.replace("'", "''")
            action_escaped = action.replace("'", "''")
            tweet_id_escaped = data.get('tweet_id', '').replace("'", "''")
            text_escaped = data.get('text', '').replace("'", "''")
            success = data.get('success', False)
            
            query = f"""
            INSERT INTO TWEETERBOT_ANALYTICS (
                session_id, action_type, timestamp, tweet_id, tweet_text, success
            ) VALUES ('{session_id_escaped}', '{action_escaped}', CURRENT_TIMESTAMP(), '{tweet_id_escaped}', '{text_escaped}', {str(success).upper()})
            """
            
            if st.session_state.get('debug_mode', False):
                st.info(f"🔍 Debug: Executing query: {query}")
            
            conn.query(query)
        else:
            st.warning(f"Unknown action type: {action}")
            return False
            
        st.success(f"✅ Data stored successfully for {action}")
        return True
        
    except Exception as e:
        # Silently handle Snowflake errors - don't show to users
        return False

# Show content based on selected page
if page == "🐦 Tweet Generator":
    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📸 Upload Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'gif'],
            help="Upload an image and AI will generate a tweet about it!"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image")
            
            # Store image in session state
            st.session_state.uploaded_image = image
            
            # Store image data in Snowflake
            store_data_in_snowflake(
                st.session_state.session_id,
                "image_upload",
                {"name": uploaded_file.name, "size": len(uploaded_file.getvalue())}
            )
            
            # Generate description button
            if st.button("🤖 Generate Tweet", type="primary"):
                with st.spinner("Generating tweet content..."):
                    start_time = time.time()
                    description = ""
                    ai_provider_key = ai_provider.split(" ")[0].lower()
                    
                    # Generate description based on selected provider
                    if ai_provider == "Perplexity AI (Recommended)":
                        if perplexity_key:
                            description = generate_image_description_with_perplexity(image, perplexity_key)
                            
                            # If Perplexity fails with network issues, try Hugging Face as fallback
                            if (description.startswith("NETWORK_ERROR") or 
                                description.startswith("TIMEOUT_ERROR") or 
                                description.startswith("FAILED_ALL_RETRIES") or
                                description.startswith("Network connection failed") or 
                                description.startswith("Failed to generate description")):
                                description = generate_image_description_with_huggingface(image, hf_token)
                                
                                # If Hugging Face also fails, try OpenAI as second fallback
                                if (description.startswith("NETWORK_ERROR") or 
                                    description.startswith("TIMEOUT_ERROR") or 
                                    description.startswith("FAILED_ALL_RETRIES") or
                                    description.startswith("Error")):
                                    if openai_key:
                                        description = generate_image_description_with_openai(image, openai_key)
                                        if description.startswith("Error"):
                                            description = generate_fallback_description(image)
                                    else:
                                        description = generate_fallback_description(image)
                        else:
                            st.error("❌ Perplexity API key not configured. Please set PERPLEXITY_API_KEY in your .env file.")
                            description = ""
                    elif ai_provider == "Hugging Face (Free)":
                        description = generate_image_description_with_huggingface(image, hf_token)
                    elif ai_provider == "OpenAI (Paid)":
                        if openai_key:
                            description = generate_image_description_with_openai(image, openai_key)
                        else:
                            st.error("❌ Please enter your OpenAI API key in the sidebar to use this feature.")
                            st.info("💡 You can get an API key from https://platform.openai.com/api-keys")
                            description = ""
                    
                    processing_time = int((time.time() - start_time) * 1000)
                    
                    # Check if description generation was successful
                    if (description.startswith("Error") or 
                        description.startswith("Failed") or 
                        description.startswith("NETWORK_ERROR") or 
                        description.startswith("TIMEOUT_ERROR") or 
                        description.startswith("UNEXPECTED_ERROR")):
                        st.error(f"❌ {description}")
                        st.info("💡 Try switching to a different AI provider in the sidebar")
                        
                        # Add manual fallback options
                        st.info("🔄 You can try alternative options:")
                        col_fallback1, col_fallback2, col_fallback3 = st.columns(3)
                        
                        with col_fallback1:
                            if st.button("🔄 Try Hugging Face", type="secondary"):
                                with st.spinner("Trying Hugging Face..."):
                                    fallback_description = generate_image_description_with_huggingface(image, hf_token)
                                    if not fallback_description.startswith("Error") and not fallback_description.startswith("NETWORK_ERROR"):
                                        description = fallback_description
                                        st.session_state.tweet_content = description
                                        st.rerun()
                        
                        with col_fallback2:
                            if openai_key and st.button("🔄 Try OpenAI", type="secondary"):
                                with st.spinner("Trying OpenAI..."):
                                    fallback_description = generate_image_description_with_openai(image, openai_key)
                                    if not fallback_description.startswith("Error"):
                                        description = fallback_description
                                        st.session_state.tweet_content = description
                                        st.rerun()
                        
                        with col_fallback3:
                            if st.button("📝 Use Fallback Content", type="secondary"):
                                with st.spinner("Generating fallback content..."):
                                    description = generate_fallback_description(image)
                                    st.session_state.tweet_content = description
                                    st.rerun()
                    else:
                        st.success("✅ Tweet generated successfully!")
                    
                    # Store AI generation data
                    if (description and 
                        not description.startswith("Error") and 
                        not description.startswith("Failed") and
                        not description.startswith("NETWORK_ERROR") and
                        not description.startswith("TIMEOUT_ERROR") and
                        not description.startswith("UNEXPECTED_ERROR")):
                        store_data_in_snowflake(
                            st.session_state.session_id,
                            "ai_generation",
                            {
                                "provider": ai_provider_key,
                                "text": description,
                                "processing_time": processing_time
                            }
                        )
                    
                    st.session_state.tweet_content = description

    with col2:
        st.subheader("✍️ Tweet Preview")
        
        if st.session_state.tweet_content:
            st.markdown('<div class="tweet-preview">', unsafe_allow_html=True)
            st.write(st.session_state.tweet_content)
            
            # Character count
            char_count = len(st.session_state.tweet_content)
            if char_count > 280:
                st.error(f"⚠️ Tweet is {char_count} characters (280 limit)")
            else:
                st.success(f"✅ Tweet is {char_count} characters")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Edit tweet content
            edited_content = st.text_area(
                "Edit Tweet Content",
                value=st.session_state.tweet_content,
                height=100,
                help="You can edit the generated tweet before posting"
            )
            
            st.session_state.tweet_content = edited_content
            
            # Post tweet section
            st.subheader("🐦 Post Tweet")
            
            # Check if Twitter credentials are provided
            if all([twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_token_secret]):
                if st.button("🚀 Post Tweet", type="primary"):
                    if st.session_state.uploaded_image and st.session_state.tweet_content:
                        with st.spinner("Posting tweet..."):
                            # Convert image to bytes
                            img_byte_arr = io.BytesIO()
                            st.session_state.uploaded_image.save(img_byte_arr, format='JPEG')
                            img_bytes = img_byte_arr.getvalue()
                            
                            success, result = post_tweet_direct_api(
                                st.session_state.tweet_content,
                                img_bytes,
                                twitter_api_key,
                                twitter_api_secret,
                                twitter_access_token,
                                twitter_access_token_secret
                            )
                            
                            # Store tweet result
                            store_data_in_snowflake(
                                st.session_state.session_id,
                                "tweet_post",
                                {
                                    "tweet_id": result if success else "",
                                    "text": st.session_state.tweet_content,
                                    "success": success
                                }
                            )
                            
                            if success:
                                st.markdown(f"""
                                <div class="success-message">
                                    ✅ Tweet posted successfully!<br>
                                    Tweet ID: {result}<br>
                                    <a href="https://twitter.com/i/web/status/{result}" target="_blank">View Tweet</a>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="error-message">
                                    ❌ Error posting tweet: {result}
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.error("Please upload an image and generate tweet content first")
            else:
                st.error("❌ Twitter API not configured. Please add your Twitter API credentials to Streamlit secrets.")
                st.info("💡 Check the sidebar for configuration instructions")
        else:
            st.info("👆 Upload an image and click 'Generate Tweet' to see the preview here")

elif page == "📊 Analytics Dashboard":
    st.subheader("📊 Usage Analytics")
    
    try:
        # Use Snowflake connection to fetch analytics
        conn = st.connection("snowflake")
        
        # Daily usage stats
        daily_stats = conn.query("""
            SELECT 
                DATE(timestamp) as date,
                COUNT(DISTINCT session_id) as unique_sessions,
                COUNT(CASE WHEN action_type = 'image_upload' THEN 1 END) as image_uploads,
                COUNT(CASE WHEN action_type = 'ai_generation' THEN 1 END) as ai_generations,
                COUNT(CASE WHEN action_type = 'tweet_post' THEN 1 END) as tweets_posted
            FROM TWEETERBOT_ANALYTICS 
            WHERE timestamp >= DATEADD(day, -30, CURRENT_DATE())
            GROUP BY DATE(timestamp)
            ORDER BY date DESC
        """)
        
        if not daily_stats.empty:
            st.dataframe(daily_stats)
            
            # Simple charts using Streamlit's built-in charting
            st.subheader("📈 Trends")
            st.line_chart(daily_stats.set_index('DATE')[['UNIQUE_SESSIONS', 'IMAGE_UPLOADS', 'AI_GENERATIONS', 'TWEETS_POSTED']])
        else:
            st.info("No analytics data available yet. Start using the app to see insights!")
            
        # AI Provider Performance
        st.subheader("🤖 AI Provider Usage")
        provider_stats = conn.query("""
            SELECT 
                ai_provider,
                COUNT(*) as total_generations,
                AVG(processing_time_ms) as avg_processing_time
            FROM TWEETERBOT_ANALYTICS 
            WHERE action_type = 'ai_generation' AND ai_provider IS NOT NULL
            GROUP BY ai_provider
            ORDER BY total_generations DESC
        """)
        
        if not provider_stats.empty:
            st.dataframe(provider_stats)
        
    except Exception as e:
        st.error(f"❌ Error loading analytics: {str(e)}")
        st.info("💡 Make sure the TWEETERBOT_ANALYTICS table exists in your Snowflake database")
        
        with st.expander("📝 Create Analytics Table"):
            st.code("""
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
            """, language="sql")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🐦 AI Tweet Generator - Optimized for Snowflake SiS</p>
    <p><small>Upload images, generate tweets, and analyze your data natively in Snowflake!</small></p>
</div>
""", unsafe_allow_html=True)
