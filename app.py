import streamlit as st
import requests
import base64
import io
from PIL import Image
import tweepy
import os
from dotenv import load_dotenv
import time
from snowflake_manager import snowflake_manager
import pandas as pd

# Load environment variables
load_dotenv()

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

# Secure credential management
def get_secret_or_env(secret_key, env_key, default=""):
    """Securely get credentials from Streamlit secrets or environment variables"""
    try:
        return st.secrets[secret_key]
    except:
        return os.getenv(env_key, default)

# Get credentials securely (not exposed to frontend)
twitter_api_key = get_secret_or_env("twitter.api_key", "TWITTER_API_KEY")
twitter_api_secret = get_secret_or_env("twitter.api_secret", "TWITTER_API_SECRET")
twitter_access_token = get_secret_or_env("twitter.access_token", "TWITTER_ACCESS_TOKEN")
twitter_access_token_secret = get_secret_or_env("twitter.access_token_secret", "TWITTER_ACCESS_TOKEN_SECRET")

perplexity_key = get_secret_or_env("ai.perplexity_api_key", "PERPLEXITY_API_KEY")
hf_token = get_secret_or_env("ai.huggingface_token", "HUGGINGFACE_TOKEN")
openai_key = get_secret_or_env("ai.openai_api_key", "OPENAI_API_KEY")

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
        with st.expander("📝 How to add Twitter API keys"):
            st.markdown("""
            **For Streamlit Cloud:**
            1. Go to your app's settings
            2. Add these secrets:
            ```
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
        if not perplexity_key:
            st.warning("⚠️ Perplexity API key not configured")
            user_perplexity_key = st.text_input(
                "Enter Perplexity API Key", 
                type="password",
                help="Get your API key from https://www.perplexity.ai/settings/api"
            )
            if user_perplexity_key:
                perplexity_key = user_perplexity_key
                st.success("✅ Perplexity API key entered")
        else:
            st.success("✅ Perplexity API configured")
            
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
    
    # Snowflake Database Status
    st.subheader("🗄️ Database")
    if st.session_state.snowflake_connected:
        st.success("✅ Snowflake connected")
        if st.session_state.snowflake_session_id:
            # Get session stats
            session_stats = snowflake_manager.get_user_session_stats(st.session_state.snowflake_session_id)
            if session_stats:
                st.info(f"📊 Session Stats: {session_stats.get('images_uploaded', 0)} images, {session_stats.get('ai_generations', 0)} AI generations, {session_stats.get('tweets_posted', 0)} tweets")
    else:
        st.warning("⚠️ Snowflake not connected")
        st.info("💡 Add Snowflake credentials to enable data storage and analytics")
        with st.expander("📝 How to configure Snowflake"):
            st.markdown("""
            **For Streamlit Cloud:**
            1. Go to your app's settings
            2. Add these secrets:
            ```
            [snowflake]
            account = "your_account"
            user = "your_username"
            password = "your_password"
            warehouse = "your_warehouse"
            database = "TWEETERBOT_DB"
            schema = "TWEET_DATA"
            role = "your_role"
            ```
            """)
    

# Initialize session state
if 'tweet_content' not in st.session_state:
    st.session_state.tweet_content = ""
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'snowflake_session_id' not in st.session_state:
    st.session_state.snowflake_session_id = ""
if 'snowflake_connected' not in st.session_state:
    st.session_state.snowflake_connected = False

# Initialize Snowflake connection
if not st.session_state.snowflake_connected:
    if snowflake_manager.connect():
        st.session_state.snowflake_connected = True
        # Create user session
        user_ip = st.context.headers.get("x-forwarded-for", "unknown")
        user_agent = st.context.headers.get("user-agent", "unknown")
        st.session_state.snowflake_session_id = snowflake_manager.create_user_session(user_ip, user_agent)

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

# def generate_image_description_with_perplexity(image, api_key):
#     """Generate image description using Perplexity AI"""
#     try:
#         import openai
        
#         # Initialize Perplexity AI client
#         client = openai.OpenAI(
#             api_key=api_key,
#             base_url="https://api.perplexity.ai"
#         )
        
#         # Convert image to base64
#         img_base64 = encode_image_to_base64(image)
        
#         # Create the image URL for the API
#         image_url = f"data:image/jpeg;base64,{img_base64}"
        
#         response = client.chat.completions.create(
#             model="sonar-pro",
#             messages=[
#                 {
#                     "role": "system", 
#                     "content": "You are a social media expert. Write engaging, concise tweets about images. Keep descriptions under 280 characters, make them interesting and social media-friendly. Focus on what makes the image unique or noteworthy."
#                 },
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": "Write a brief, engaging tweet about this image. Make it interesting for social media and keep it under 280 characters."},
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": image_url
#                             }
#                         }
#                     ]
#                 }
#             ],
#             max_tokens=150,
#             temperature=0.7
#         )
        
#         return response.choices[0].message.content.strip()
        
#     except Exception as e:
#         return f"Error generating description with Perplexity AI: {str(e)}"

def generate_image_description_with_perplexity(image, api_key):
    """Generate a short and impactful complaint tweet about road conditions using Perplexity AI"""
    try:
        import openai

        # Initialize Perplexity AI client
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )

        # Convert image to base64
        img_base64 = encode_image_to_base64(image)

        # Create the image URL for the API
        image_url = f"data:image/jpeg;base64,{img_base64}"

        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "system",
                    "content": "You are a social media expert. Write engaging, concise tweets about images. Keep descriptions under 280 characters, make them interesting and social media-friendly. Focus on what makes the image unique or noteworthy."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Write a brief, engaging tweet about this image. Make it interesting for social media and keep it under 280 characters."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        }
                    ]
                }
            ],
            max_tokens=150,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating description with Perplexity AI: {str(e)}"


def generate_image_description_with_huggingface(image, token=""):
    """Generate image description using Hugging Face's free API"""
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
            data=img_base64,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'No description generated')
            else:
                return result.get('generated_text', 'No description generated')
        else:
            return f"API Error: {response.status_code}"
            
    except Exception as e:
        return f"Error generating description: {str(e)}"

def generate_image_description_with_openai(image, api_key):
    """Generate image description using OpenAI API"""
    try:
        import openai
        
        openai.api_key = api_key
        
        # Convert image to base64
        img_base64 = encode_image_to_base64(image)
        
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Write a brief, engaging tweet about this image. Keep it under 280 characters and make it interesting for social media."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=150
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating description: {str(e)}"

def generate_image_description_with_custom_api(image, api_url, api_key):
    """Generate image description using custom API"""
    try:
        img_base64 = encode_image_to_base64(image)
        
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        payload = {
            "image": img_base64,
            "prompt": "Write a brief, engaging tweet about this image. Keep it under 280 characters."
        }
        
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('description', result.get('text', 'No description generated'))
        else:
            return f"API Error: {response.status_code}"
            
    except Exception as e:
        return f"Error generating description: {str(e)}"

def post_tweet(content, image_path, api_key, api_secret, access_token, access_token_secret):
    """Post tweet with text and image"""
    try:
        # Initialize Twitter API
        auth = tweepy.OAuth1UserHandler(
            api_key, api_secret, access_token, access_token_secret
        )
        api = tweepy.API(auth)
        
        # Upload image
        media = api.media_upload(image_path)
        
        # Post tweet with media
        tweet = api.update_status(status=content, media_ids=[media.media_id])
        
        return True, tweet.id_str
        
    except Exception as e:
        return False, str(e)

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
        st.image(image, caption="Uploaded Image", width='stretch')
        
        # Store image in session state
        st.session_state.uploaded_image = image
        
        # Store image in Snowflake if connected
        if st.session_state.snowflake_connected and st.session_state.snowflake_session_id:
            try:
                # Convert image to bytes
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_bytes = img_byte_arr.getvalue()
                
                # Store in Snowflake
                image_id = snowflake_manager.store_uploaded_image(
                    st.session_state.snowflake_session_id,
                    img_bytes,
                    uploaded_file.name,
                    image.format or 'JPEG',
                    image.width,
                    image.height
                )
                
                if image_id:
                    st.session_state.current_image_id = image_id
                    # Log analytics event
                    snowflake_manager.log_analytics_event(
                        st.session_state.snowflake_session_id,
                        'image_upload',
                        success=True
                    )
                    st.success("📊 Image stored in database")
                    
            except Exception as e:
                st.warning(f"Could not store image in database: {str(e)}")
                snowflake_manager.log_analytics_event(
                    st.session_state.snowflake_session_id,
                    'image_upload',
                    success=False,
                    error_type=str(e)
                )
        
        # Generate description button
        if st.button("🤖 Generate Tweet", type="primary"):
            with st.spinner("Generating tweet content..."):
                start_time = time.time()
                description = ""
                ai_provider_key = ai_provider.split(" ")[0].lower()  # Extract provider name
                
                # Generate description based on selected provider
                if ai_provider == "Perplexity AI (Recommended)":
                    if perplexity_key:
                        description = generate_image_description_with_perplexity(image, perplexity_key)
                    else:
                        st.error("❌ Please enter your Perplexity API key in the sidebar to use this feature.")
                        st.info("💡 You can get a free API key from https://www.perplexity.ai/settings/api")
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
                
                processing_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds
                
                # Store AI-generated content in Snowflake
                if description and st.session_state.snowflake_connected and hasattr(st.session_state, 'current_image_id'):
                    try:
                        # Estimate API cost (rough estimates)
                        cost_estimates = {
                            'perplexity': 0.002,
                            'openai': 0.01,
                            'hugging': 0.0
                        }
                        estimated_cost = cost_estimates.get(ai_provider_key, 0.0)
                        
                        content_id = snowflake_manager.store_ai_generated_content(
                            st.session_state.current_image_id,
                            ai_provider_key,
                            description,
                            processing_time,
                            estimated_cost
                        )
                        
                        if content_id:
                            st.session_state.current_content_id = content_id
                            # Log analytics event
                            snowflake_manager.log_analytics_event(
                                st.session_state.snowflake_session_id,
                                'ai_generation',
                                ai_provider_key,
                                success=True,
                                processing_time_ms=processing_time
                            )
                            st.success(f"📊 AI content stored (took {processing_time}ms)")
                    except Exception as e:
                        st.warning(f"Could not store AI content: {str(e)}")
                        snowflake_manager.log_analytics_event(
                            st.session_state.snowflake_session_id,
                            'ai_generation',
                            ai_provider_key,
                            success=False,
                            error_type=str(e),
                            processing_time_ms=processing_time
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
                        # Save image temporarily
                        temp_image_path = "temp_image.jpg"
                        st.session_state.uploaded_image.save(temp_image_path)
                        
                        success, result = post_tweet(
                            st.session_state.tweet_content,
                            temp_image_path,
                            twitter_api_key,
                            twitter_api_secret,
                            twitter_access_token,
                            twitter_access_token_secret
                        )
                        
                        # Clean up temporary file
                        if os.path.exists(temp_image_path):
                            os.remove(temp_image_path)
                        
                        # Store tweet result in Snowflake
                        if st.session_state.snowflake_connected and hasattr(st.session_state, 'current_content_id'):
                            try:
                                tweet_record_id = snowflake_manager.store_posted_tweet(
                                    st.session_state.current_content_id,
                                    result if success else "",
                                    st.session_state.tweet_content,
                                    success,
                                    result if not success else ""
                                )
                                
                                # Log analytics event
                                snowflake_manager.log_analytics_event(
                                    st.session_state.snowflake_session_id,
                                    'tweet_post',
                                    success=success,
                                    error_type=result if not success else ""
                                )
                                
                                if tweet_record_id:
                                    st.success("📊 Tweet data stored in database")
                                    
                            except Exception as e:
                                st.warning(f"Could not store tweet data: {str(e)}")
                        
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
            st.error("❌ Twitter API not configured. Please add your Twitter API credentials to environment variables or Streamlit secrets.")
            st.info("💡 Check the sidebar for configuration instructions")
    else:
        st.info("👆 Upload an image and click 'Generate Tweet' to see the preview here")

elif page == "📊 Analytics Dashboard":
    # Import and show analytics dashboard
    try:
        from analytics_dashboard import show_analytics_dashboard, show_data_export
        
        # Main analytics content
        show_analytics_dashboard()
        
        # Data export section
        st.divider()
        show_data_export()
        
    except ImportError:
        st.error("❌ Analytics dashboard not available. Please ensure analytics_dashboard.py is in the project directory.")
    except Exception as e:
        st.error(f"❌ Error loading analytics dashboard: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🐦 AI Tweet Generator - Powered by Streamlit & Snowflake</p>
    <p><small>Upload images, generate tweets, and analyze your data!</small></p>
</div>
""", unsafe_allow_html=True)
