# Deployment Guide

This guide will help you deploy your Streamlit portfolio to various platforms.

## 🚀 Quick Deployment Options

### Option 1: Streamlit Community Cloud (Recommended)

**Steps:**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository
6. Set main file path: `portfolio_app.py`
7. Click "Deploy"

**Pros:**
- Free hosting
- Automatic deployments from GitHub
- Easy to use
- Built for Streamlit apps

### Option 2: Heroku

**Steps:**
1. Create a `Procfile`:
   ```
   web: streamlit run portfolio_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [general]\n\
   email = \"your-email@domain.com\"\n\
   " > ~/.streamlit/credentials.toml
   echo "\
   [server]\n\
   headless = true\n\
   enableCORS=false\n\
   port = $PORT\n\
   " > ~/.streamlit/config.toml
   ```

3. Deploy to Heroku:
   ```bash
   heroku create your-portfolio-name
   git push heroku main
   ```

### Option 3: Railway

**Steps:**
1. Connect your GitHub repository to Railway
2. Set the start command: `streamlit run portfolio_app.py --server.port=$PORT --server.address=0.0.0.0`
3. Deploy automatically

### Option 4: Google Cloud Platform

**Steps:**
1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "portfolio_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. Deploy using Cloud Run:
   ```bash
   gcloud run deploy --source .
   ```

## 📸 Adding Your Profile Photo

### Method 1: Direct Upload
1. Add your photo to the project directory as `profile_photo.jpg`
2. Ensure it's a square image (recommended: 400x400 pixels)
3. The app will automatically detect and use it

### Method 2: Generate Placeholder
1. Run the placeholder generator:
   ```bash
   python profile_image_placeholder.py
   ```
2. This creates a professional placeholder with your initials

### Method 3: Online Image
1. Host your image on a CDN or image hosting service
2. Update the `load_profile_image()` function to use the URL

## 🔧 Customization

### Updating Personal Information

Edit these sections in `portfolio_app.py`:

1. **Header Information** (lines 112-113):
   ```python
   st.markdown('<h1 class="main-header">Your Name</h1>', unsafe_allow_html=True)
   st.markdown('<p class="sub-header">Your Title | Your Specialization</p>', unsafe_allow_html=True)
   ```

2. **About Section** (around line 130):
   - Update the professional summary
   - Modify key metrics

3. **Experience** (around line 180):
   - Update the `experiences` list with your work history

4. **Skills** (around line 220):
   - Modify the `skills_data` dictionary

5. **Projects** (around line 280):
   - Update the `projects` list with your work

6. **Contact** (around line 350):
   - Update contact information and links

### Styling Customization

Modify the CSS in the `st.markdown()` section (lines 15-80) to:
- Change colors
- Update fonts
- Modify layout
- Add animations

## 🚀 GitHub Actions for Automated Deployment

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        streamlit run portfolio_app.py --server.headless true --server.port 8501
```

## 📊 Performance Optimization

### Image Optimization
- Use WebP format for better compression
- Optimize image sizes (max 400x400 for profile photo)
- Use lazy loading for multiple images

### Code Optimization
- Minimize external API calls
- Use caching for expensive operations
- Optimize CSS and JavaScript

### Deployment Optimization
- Use CDN for static assets
- Enable gzip compression
- Set proper cache headers

## 🔍 Monitoring and Analytics

### Add Google Analytics
```python
# Add to the beginning of portfolio_app.py
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)
```

### Streamlit Analytics
- Enable in Streamlit Community Cloud settings
- Monitor app usage and performance

## 🛠️ Troubleshooting

### Common Issues

1. **App won't start locally:**
   - Check Python version (3.8+)
   - Verify all dependencies are installed
   - Check for syntax errors

2. **Deployment fails:**
   - Ensure `requirements.txt` is up to date
   - Check file paths are correct
   - Verify all imports are available

3. **Images not loading:**
   - Check file paths
   - Ensure images are in the correct directory
   - Verify image formats are supported

4. **Styling issues:**
   - Check CSS syntax
   - Verify HTML structure
   - Test in different browsers

### Getting Help

- Check Streamlit documentation
- Visit Streamlit community forum
- Review GitHub issues
- Contact support

## 📈 Next Steps

After deployment:
1. Share your portfolio URL
2. Add to your LinkedIn profile
3. Include in your resume
4. Share on social media
5. Collect feedback and iterate

---

**Happy Deploying! 🚀**
