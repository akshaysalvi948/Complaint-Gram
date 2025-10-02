# 🔧 Streamlit Cloud Deployment Troubleshooting

If you're getting "Error installing requirements" on Streamlit Cloud, here are the solutions:

## 🚨 Quick Fixes

### 1. **Requirements.txt Issues**

**Problem**: Version conflicts or incompatible packages
**Solution**: Use the simplified requirements.txt (already updated):

```
streamlit
requests
Pillow
tweepy
python-dotenv
openai
```

### 2. **Python Version Issues**

**Problem**: Unsupported Python version
**Solution**: Use Python 3.11 (already updated in runtime.txt):

```
python-3.11
```

### 3. **System Packages Issues**

**Problem**: Too many or incompatible system packages
**Solution**: Minimal packages.txt (already updated):

```
libgl1-mesa-glx
libglib2.0-0
```

## 📋 Step-by-Step Deployment Fix

### Option 1: Redeploy with Fixed Files

1. **Go to your Streamlit Cloud dashboard**
2. **Delete the current app** (if it exists)
3. **Create a new app** with these settings:
   - Repository: `akshaysalvi948/Complaint-Gram`
   - Branch: `main`
   - Main file: `app.py`

### Option 2: Force Refresh

1. **Go to your app's "Manage" page**
2. **Click "Reboot app"**
3. **Wait for fresh deployment**

### Option 3: Check Logs

1. **Click "Manage App"** in Streamlit Cloud
2. **Check the terminal logs** for specific errors
3. **Look for these common issues**:

## 🐛 Common Error Messages & Solutions

### Error: "Could not find a version that satisfies the requirement"

**Cause**: Version conflicts
**Fix**: Remove version pinning from requirements.txt

```bash
# Instead of:
streamlit==1.28.1

# Use:
streamlit
```

### Error: "Failed building wheel for [package]"

**Cause**: Missing system dependencies
**Fix**: Check packages.txt has required libraries

### Error: "No module named 'PIL'"

**Cause**: Pillow installation issue
**Fix**: Use `Pillow` (capital P) in requirements.txt

### Error: "ImportError: libGL.so.1"

**Cause**: Missing OpenGL libraries
**Fix**: Add to packages.txt:
```
libgl1-mesa-glx
```

## 🔄 Alternative Deployment Methods

If Streamlit Cloud continues to have issues, try these alternatives:

### 1. **Railway** (Free tier available)
```bash
# Connect GitHub repo to Railway
# Set environment variables in Railway dashboard
# Deploy automatically
```

### 2. **Render** (Free tier available)
```bash
# Build Command: pip install -r requirements.txt
# Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

### 3. **Heroku** (Paid)
```bash
heroku create your-app-name
git push heroku main
```

## 🔍 Debug Your Deployment

### Check Your Files

Run this locally to validate everything:
```bash
python deploy.py
```

### Minimal Test App

Create a simple test to isolate issues:

**test_app.py**:
```python
import streamlit as st
st.write("Hello World!")
```

**test_requirements.txt**:
```
streamlit
```

Deploy this first, then gradually add features.

## 📞 Getting Help

### Streamlit Community
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Discord](https://discord.gg/streamlit)

### GitHub Issues
- Check if others have similar issues
- Create new issue with error logs

### Alternative Support
- Try deployment on different platforms
- Use local development while troubleshooting

## ✅ Verification Checklist

Before deploying, ensure:

- [ ] requirements.txt has no version conflicts
- [ ] packages.txt is minimal
- [ ] runtime.txt specifies supported Python version
- [ ] All files are committed to GitHub
- [ ] Secrets are configured in Streamlit Cloud dashboard
- [ ] App runs locally without errors

## 🎯 Success Tips

1. **Keep it simple**: Start with minimal dependencies
2. **Test locally first**: Always verify locally before deploying
3. **Check logs**: Read error messages carefully
4. **Use latest versions**: Keep Streamlit and dependencies updated
5. **Monitor resources**: Watch for memory/CPU limits

---

**Your TweeterBot should now deploy successfully! 🚀**

If you still have issues, the problem might be temporary with Streamlit Cloud servers. Try again in a few hours or use an alternative platform.
