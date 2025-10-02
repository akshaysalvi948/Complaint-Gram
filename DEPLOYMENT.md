# 🚀 Deployment Guide - AI Tweet Generator Bot

This guide will help you deploy your TweeterBot to the internet using various platforms. The easiest and recommended method is Streamlit Cloud (free).

## 🌟 Streamlit Cloud Deployment (Recommended - FREE)

### Prerequisites
- GitHub account with your code pushed
- Twitter Developer Account with API credentials
- Optional: AI API keys (Perplexity, OpenAI, etc.)

### Step-by-Step Deployment

#### 1. Prepare Your Repository
Your repository should already have these files:
```
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml.example # Secrets template
├── packages.txt             # System packages
├── runtime.txt              # Python version
└── README.md                # Documentation
```

#### 2. Deploy to Streamlit Cloud

1. **Visit Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select your repository: `akshaysalvi948/Complaint-Gram`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: Choose a custom URL (e.g., `ai-tweet-generator`)

3. **Configure Secrets**
   - Click "Advanced settings"
   - In the "Secrets" section, paste your configuration:

   ```toml
   [twitter]
   api_key = "your_actual_twitter_api_key"
   api_secret = "your_actual_twitter_api_secret"
   access_token = "your_actual_twitter_access_token"
   access_token_secret = "your_actual_twitter_access_token_secret"

   [ai]
   perplexity_api_key = "your_actual_perplexity_key"
   # Add other AI keys as needed
   ```

4. **Deploy**
   - Click "Deploy!"
   - Wait for deployment (usually 2-5 minutes)
   - Your app will be live at: `https://your-app-name.streamlit.app`

#### 3. Post-Deployment Setup

1. **Test Your App**
   - Visit your deployed URL
   - Test image upload and AI generation
   - Verify Twitter posting works

2. **Update Twitter App Settings**
   - Go to [Twitter Developer Portal](https://developer.twitter.com/)
   - Update your app's callback URLs to include your Streamlit URL
   - Ensure permissions are set to "Read and Write"

3. **Monitor Usage**
   - Check Streamlit Cloud dashboard for app metrics
   - Monitor API usage and costs

### 🔧 Troubleshooting Streamlit Cloud

#### Common Issues

**App Won't Start**
- Check logs in Streamlit Cloud dashboard
- Verify all dependencies in `requirements.txt`
- Ensure Python version compatibility

**Secrets Not Working**
- Verify secrets format in Streamlit dashboard
- Check for typos in secret keys
- Ensure secrets match the format in your code

**Image Upload Issues**
- Check file size limits (5MB max)
- Verify supported formats in your code
- Test with smaller images first

**API Errors**
- Verify API credentials are correct
- Check API quotas and limits
- Test APIs independently

## 🐳 Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    libgl1-mesa-glx \\
    libglib2.0-0 \\
    libsm6 \\
    libxext6 \\
    libxrender-dev \\
    libgomp1 \\
    fonts-liberation \\
    libfontconfig1 \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  tweeterbot:
    build: .
    ports:
      - "8501:8501"
    environment:
      - TWITTER_API_KEY=${TWITTER_API_KEY}
      - TWITTER_API_SECRET=${TWITTER_API_SECRET}
      - TWITTER_ACCESS_TOKEN=${TWITTER_ACCESS_TOKEN}
      - TWITTER_ACCESS_TOKEN_SECRET=${TWITTER_ACCESS_TOKEN_SECRET}
      - PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

### Deploy with Docker
```bash
# Build and run
docker build -t tweeterbot .
docker run -p 8501:8501 --env-file .env tweeterbot

# Or use docker-compose
docker-compose up -d
```

## ☁️ Heroku Deployment

### 1. Prepare Heroku Files

**Procfile**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt** (already created)
```
python-3.9
```

### 2. Deploy to Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-tweeterbot-app

# Set environment variables
heroku config:set TWITTER_API_KEY=your_key
heroku config:set TWITTER_API_SECRET=your_secret
heroku config:set TWITTER_ACCESS_TOKEN=your_token
heroku config:set TWITTER_ACCESS_TOKEN_SECRET=your_token_secret
heroku config:set PERPLEXITY_API_KEY=your_perplexity_key

# Deploy
git push heroku main

# Open your app
heroku open
```

## 🌐 Other Deployment Options

### Railway
1. Connect GitHub repository
2. Add environment variables
3. Deploy automatically

### Render
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### DigitalOcean App Platform
1. Create new app from GitHub
2. Configure environment variables
3. Deploy with automatic scaling

## 🔒 Security Considerations

### Environment Variables
- Never commit API keys to version control
- Use platform-specific secret management
- Rotate keys regularly
- Monitor API usage

### HTTPS
- Most platforms provide HTTPS automatically
- Ensure all API calls use HTTPS
- Validate SSL certificates

### Rate Limiting
- Implement client-side rate limiting
- Monitor API quotas
- Handle rate limit errors gracefully

## 📊 Monitoring & Analytics

### Streamlit Cloud
- Built-in analytics dashboard
- Usage metrics and logs
- Performance monitoring

### Custom Monitoring
```python
import logging
import time
from datetime import datetime

# Add to your app.py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_usage(action, user_info=None):
    logger.info(f"{datetime.now()}: {action} - {user_info}")

# Use throughout your app
log_usage("image_uploaded", {"size": image.size})
log_usage("tweet_generated", {"ai_provider": provider})
log_usage("tweet_posted", {"success": True})
```

### Error Tracking
```python
import traceback

try:
    # Your code here
    pass
except Exception as e:
    logger.error(f"Error: {str(e)}")
    logger.error(traceback.format_exc())
    st.error("Something went wrong. Please try again.")
```

## 🚀 Performance Optimization

### Caching
```python
@st.cache_data
def load_ai_model():
    # Cache expensive operations
    return model

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_api_response(image_data):
    # Cache API responses
    return response
```

### Image Optimization
```python
from PIL import Image

def optimize_image(image, max_size=(1024, 1024), quality=85):
    if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image
```

## 📈 Scaling Considerations

### Traffic Management
- Use CDN for static assets
- Implement caching strategies
- Consider load balancing for high traffic

### Database Integration
- Add user analytics
- Store tweet history
- Implement user preferences

### API Management
- Implement API key rotation
- Add fallback providers
- Monitor and alert on failures

## 🎯 Next Steps After Deployment

1. **Test Thoroughly**
   - Upload various image types
   - Test all AI providers
   - Verify Twitter integration

2. **Monitor Performance**
   - Check response times
   - Monitor error rates
   - Track user engagement

3. **Gather Feedback**
   - Add feedback forms
   - Monitor user behavior
   - Iterate based on usage

4. **Scale as Needed**
   - Upgrade hosting plans
   - Add more AI providers
   - Implement advanced features

## 📞 Support

If you encounter issues during deployment:

1. **Check Logs**: Always start with application logs
2. **Verify Credentials**: Ensure all API keys are correct
3. **Test Locally**: Reproduce issues in local environment
4. **Platform Documentation**: Check platform-specific guides
5. **Community Support**: Use platform community forums

---

**Your TweeterBot is ready for the world! 🌍✨**

*Choose the deployment method that best fits your needs and budget.*
