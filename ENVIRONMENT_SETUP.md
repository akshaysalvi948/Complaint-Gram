# Environment Variables Setup for Snowflake SiS

This guide explains how to set up environment variables for the TweeterBot app in Snowflake Streamlit in Snowflake (SiS).

## Required Environment Variables

### Perplexity AI API Key (Required)
```
PERPLEXITY_API_KEY=your_perplexity_api_key_here
```

**How to get your API key:**
1. Visit https://www.perplexity.ai/settings/api
2. Sign up or log in to your account
3. Generate a new API key
4. Copy the key and set it as an environment variable

### Optional Environment Variables

#### Hugging Face API Key (Optional)
```
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

#### OpenAI API Key (Optional)
```
OPENAI_API_KEY=your_openai_api_key_here
```

#### Twitter API Keys (Optional)
```
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here
```

## Setting Environment Variables in Snowflake SiS

### Method 1: Using Snowflake UI
1. Go to your Snowflake Streamlit app
2. Navigate to the app settings
3. Find the "Environment Variables" section
4. Add the required variables:
   - Key: `PERPLEXITY_API_KEY`
   - Value: `your_actual_api_key_here`

### Method 2: Using SQL (if supported)
```sql
-- Set environment variable (syntax may vary by Snowflake version)
ALTER APPLICATION PACKAGE your_app_package 
SET ENVIRONMENT_VARIABLE PERPLEXITY_API_KEY = 'your_api_key_here';
```

### Method 3: Using Snowflake CLI (if available)
```bash
snow app set-env PERPLEXITY_API_KEY=your_api_key_here
```

## Local Development Setup

For local development, create a `.env` file in your project root:

```bash
# .env file
PERPLEXITY_API_KEY=your_perplexity_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here
```

## Verification

After setting the environment variables:

1. **Check the sidebar**: The app will show "✅ Perplexity API configured (loaded from environment)" if the key is found
2. **Test functionality**: Try uploading an image and generating a tweet
3. **Check logs**: Look for any error messages related to missing API keys

## Troubleshooting

### Common Issues

1. **"Perplexity API key not found"**
   - Verify the environment variable is set correctly
   - Check for typos in the variable name
   - Ensure the variable is set in the correct environment

2. **"API key invalid"**
   - Verify the API key is correct
   - Check if the key has expired
   - Ensure the key has the necessary permissions

3. **Environment variable not loading**
   - Restart the Streamlit app after setting variables
   - Check if the variable name matches exactly (case-sensitive)
   - Verify the variable is set in the correct scope

## Security Notes

- **Never commit API keys to version control**
- **Use environment variables for sensitive data**
- **Rotate API keys regularly**
- **Monitor API usage and costs**

## Support

If you encounter issues:
1. Check the app logs for error messages
2. Verify all required environment variables are set
3. Test with a simple API call to verify connectivity
4. Contact your Snowflake administrator for environment variable setup help
