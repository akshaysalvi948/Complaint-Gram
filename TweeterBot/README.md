# 🐦 AI Tweet Generator

A beautiful Streamlit application that allows you to upload images and automatically generate engaging tweets about them using AI, then post them directly to Twitter.

## ✨ Features

- **📸 Image Upload**: Upload images in PNG, JPG, JPEG, or GIF formats
- **🤖 AI-Powered Descriptions**: Multiple AI providers supported:
  - **Perplexity AI (Recommended)**: High-quality image descriptions with fast response times
  - **Hugging Face (Free)**: Uses Salesforce's BLIP model for image captioning
  - **OpenAI (Paid)**: Uses GPT-4 Vision for more sophisticated descriptions
  - **Custom API**: Support for your own AI API endpoints
- **✍️ Tweet Editing**: Edit the generated tweet content before posting
- **🐦 Direct Twitter Posting**: Post tweets with images directly to your Twitter account
- **📊 Character Counter**: Real-time character count with Twitter's 280-character limit
- **🎨 Beautiful UI**: Modern, responsive design with custom styling

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Twitter API

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app and get your API credentials:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret

### 3. Configure Environment Variables (Optional)

Create a `.env` file in the project root:

```bash
cp config.env.example .env
```

Then edit `.env` with your actual API keys:

```env
TWITTER_API_KEY=your_actual_api_key
TWITTER_API_SECRET=your_actual_api_secret
TWITTER_ACCESS_TOKEN=your_actual_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_actual_access_token_secret

# Optional AI API keys
PERPLEXITY_API_KEY=your_perplexity_api_key
HUGGINGFACE_TOKEN=your_huggingface_token
OPENAI_API_KEY=your_openai_api_key
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🎯 How to Use

1. **Configure APIs**: In the sidebar, enter your Twitter API credentials and choose an AI provider
2. **Upload Image**: Drag and drop or select an image file
3. **Generate Tweet**: Click "Generate Tweet" to let AI create a description
4. **Edit Content**: Review and edit the generated tweet if needed
5. **Post Tweet**: Click "Post Tweet" to publish it to your Twitter account

## 🔧 Configuration Options

### AI Providers

#### Perplexity AI (Recommended)
- **Model**: Sonar Pro with vision capabilities
- **Cost**: Pay-per-use (competitive pricing)
- **Best for**: High-quality, engaging social media descriptions with fast response times

#### Hugging Face (Free)
- **Model**: Salesforce BLIP image captioning
- **Cost**: Free (with optional token for higher rate limits)
- **Best for**: Quick, simple image descriptions

#### OpenAI (Paid)
- **Model**: GPT-4 Vision
- **Cost**: Pay-per-use
- **Best for**: More sophisticated, contextual descriptions

#### Custom API
- **Flexibility**: Use your own AI model
- **Format**: Expects JSON with `image` (base64) and `prompt` fields
- **Response**: Should return `description` or `text` field

### Twitter API Setup

1. **Create Twitter App**:
   - Go to [Twitter Developer Portal](https://developer.twitter.com/)
   - Create a new project and app
   - Generate API keys and tokens

2. **Required Permissions**:
   - Read and Write permissions
   - Media upload permissions

3. **Environment Variables**:
   - Can be set in `.env` file or entered directly in the UI
   - UI input takes precedence over environment variables

## 📁 Project Structure

```
TweeterBot/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── config.env.example    # Environment variables template
├── README.md             # This file
└── .env                  # Your actual environment variables (create this)
```

## 🛠️ Dependencies

- **streamlit**: Web application framework
- **requests**: HTTP requests for AI APIs
- **pillow**: Image processing
- **tweepy**: Twitter API integration
- **python-dotenv**: Environment variable management
- **openai**: OpenAI API client (optional)

## 🔒 Security Notes

- **API Keys**: Never commit your `.env` file to version control
- **Environment Variables**: The app supports both `.env` files and direct UI input
- **Image Processing**: Images are processed locally and temporarily stored
- **Rate Limits**: Be aware of API rate limits for both Twitter and AI services

## 🐛 Troubleshooting

### Common Issues

1. **Twitter API Errors**:
   - Verify your API credentials are correct
   - Check that your app has read/write permissions
   - Ensure your Twitter account is verified if required

2. **AI Generation Errors**:
   - Hugging Face API might be slow or rate-limited
   - Check your internet connection
   - Verify API keys if using paid services

3. **Image Upload Issues**:
   - Supported formats: PNG, JPG, JPEG, GIF
   - Maximum file size depends on your Streamlit configuration

### Getting Help

- Check the console output for detailed error messages
- Verify all API credentials are correctly entered
- Test with smaller images first

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Cloud Deployment
This app can be deployed to:
- **Streamlit Cloud**: Push to GitHub and deploy directly
- **Heroku**: Use the included `requirements.txt`
- **AWS/Azure/GCP**: Deploy as a containerized application

### Environment Variables for Production
Set these in your deployment platform:
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `PERPLEXITY_API_KEY` (optional)
- `HUGGINGFACE_TOKEN` (optional)
- `OPENAI_API_KEY` (optional)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

- This tool is for educational and personal use
- Be respectful when posting to social media
- Follow Twitter's terms of service
- Use AI-generated content responsibly
