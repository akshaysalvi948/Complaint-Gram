# 🐦 TweeterBot - AI-Powered Image-to-Tweet Generator

A powerful Streamlit application that transforms images into engaging tweets using multiple AI providers. Deployed on Snowflake Streamlit in Snowflake (SiS) with custom domain at **raiseyourvoice.co.in**.

## 🌟 Features

- **Multiple AI Providers**: Perplexity AI (recommended), Hugging Face (free), OpenAI (premium)
- **Smart Image Analysis**: Advanced AI-powered image description generation
- **Twitter Integration**: Direct posting to Twitter/X with OAuth 1.0a
- **Snowflake Analytics**: Comprehensive data storage and analytics dashboard
- **Fallback Systems**: Robust error handling with multiple fallback options
- **Mobile Responsive**: Works seamlessly on all devices
- **Custom Domain**: Professional deployment at raiseyourvoice.co.in

## 🚀 Live Application

**🌐 Access the application at: [https://raiseyourvoice.co.in](https://raiseyourvoice.co.in)**

- **Main Domain**: https://raiseyourvoice.co.in
- **WWW Subdomain**: https://www.raiseyourvoice.co.in
- **Snowflake Direct**: https://GMOFVVK-QA77419.snowflakecomputing.com/app/TweeterBot

## 🏗️ Architecture Overview

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   End Users     │    │  Custom Domain  │    │  Snowflake SiS  │
│                 │    │                 │    │                 │
│  Mobile/Desktop │───▶│ raiseyourvoice  │───▶│  Streamlit App  │
│  Browsers       │    │    .co.in       │    │   (TweeterBot)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Cloudflare    │
                       │                 │
                       │  SSL + CDN +    │
                       │  Redirects      │
                       └─────────────────┘
```

### Data Flow Architecture
```
Image Upload → AI Processing → Tweet Generation → Data Storage → Twitter Posting
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
┌─────────┐   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│Streamlit│   │Perplexity AI│  │Content      │  │Snowflake    │  │Twitter API  │
│   UI    │   │Hugging Face │  │Optimization │  │Analytics DB │  │OAuth 1.0a  │
│         │   │OpenAI       │  │             │  │             │  │             │
└─────────┘   └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

## 🛠️ Technology Stack

### Frontend & UI
- **Streamlit**: Modern web application framework
- **Responsive Design**: Mobile-first approach
- **Interactive Components**: Drag-and-drop, real-time preview
- **Custom Styling**: Professional UI with Twitter-inspired theme

### AI & Machine Learning
- **Perplexity AI**: Primary provider for high-quality image analysis
- **Hugging Face**: Free alternative with BLIP image captioning
- **OpenAI GPT-4 Vision**: Premium option with advanced capabilities
- **Image Processing**: PIL/Pillow for image handling and optimization

### Backend & Infrastructure
- **Snowflake Streamlit in Snowflake (SiS)**: Native cloud deployment
- **Snowflake Database**: TWEETERBOT_DB with TWEET_DATA schema
- **Custom Domain**: raiseyourvoice.co.in (GoDaddy + Cloudflare)
- **SSL Certificates**: Automatic HTTPS with Cloudflare

### Data & Analytics
- **Real-time Analytics**: Usage tracking and performance monitoring
- **Session Management**: User interaction analytics
- **AI Performance Metrics**: Success rates by provider
- **Cost Tracking**: API usage and optimization

## 🌐 Domain Configuration

### DNS Setup
- **Domain**: raiseyourvoice.co.in
- **Registrar**: GoDaddy
- **DNS Management**: Cloudflare
- **SSL**: Cloudflare SSL certificates
- **CDN**: Global content delivery

### IP Addresses
- **Primary**: 13.228.155.161
- **Secondary**: 54.179.32.193
- **Tertiary**: 18.142.35.241

### Redirect Configuration
- **Main Domain**: raiseyourvoice.co.in → Snowflake App
- **WWW Subdomain**: www.raiseyourvoice.co.in → Snowflake App
- **HTTPS Enforcement**: Automatic redirect from HTTP to HTTPS

## 📊 Analytics & Monitoring

### Key Metrics Tracked
- **Usage Statistics**: Daily/monthly active users
- **AI Performance**: Success rates by provider (Perplexity, Hugging Face, OpenAI)
- **Content Analytics**: Tweet generation success rates
- **Cost Tracking**: API usage and associated costs
- **Error Monitoring**: System health and reliability metrics

### Data Storage Schema
```sql
TWEETERBOT_ANALYTICS Table:
- session_id: STRING
- action_type: STRING
- timestamp: TIMESTAMP_TZ
- image_name: STRING
- image_size: INTEGER
- ai_provider: STRING
- tweet_content: STRING
- success: BOOLEAN
- error_message: STRING
```

## 🔧 Configuration & Setup

### Environment Variables
```bash
# Perplexity AI (Required)
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# Hugging Face (Optional)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# OpenAI (Optional)
OPENAI_API_KEY=your_openai_api_key_here

# Twitter API (Optional)
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here
```

### Snowflake Configuration
- **Account**: GMOFVVK-QA77419
- **Database**: TWEETERBOT_DB
- **Schema**: TWEET_DATA
- **Warehouse**: COMPUTE_WH
- **Role**: ACCOUNTADMIN
- **User**: akshaycdac948

## 🚀 Deployment Architecture

### Snowflake Streamlit in Snowflake (SiS)
1. **App Deployment**: Native Streamlit app in Snowflake cloud
2. **File Upload**: streamlit_app.py and requirements.txt
3. **Secret Management**: API keys stored in Snowflake secrets
4. **Public Access**: App accessible via Snowflake URL

### Custom Domain Integration
1. **Domain Registration**: raiseyourvoice.co.in via GoDaddy
2. **DNS Configuration**: A records pointing to Snowflake IPs
3. **Cloudflare Setup**: SSL certificates and redirect management
4. **Public Access**: https://raiseyourvoice.co.in

### Infrastructure Components
- **Load Balancer**: Snowflake's AWS load balancer
- **CDN**: Cloudflare global content delivery
- **SSL Termination**: Cloudflare SSL certificates
- **DNS Resolution**: Multi-IP load balancing

## 📱 User Experience

### For End Users
1. **Visit**: https://raiseyourvoice.co.in
2. **Upload Image**: Drag and drop or click to upload
3. **Select AI Provider**: Choose from available options
4. **Generate Tweet**: AI creates engaging content
5. **Post to Twitter**: Optional direct posting
6. **View Analytics**: Track usage and performance

### For Developers
1. **Clone Repository**: Get the source code
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Configure Environment**: Set up API keys
4. **Run Locally**: `streamlit run app.py`
5. **Deploy**: Follow Snowflake deployment guide

## 🔒 Security & Privacy

### Security Measures
- **HTTPS Enforcement**: All traffic encrypted
- **API Key Security**: Stored in Snowflake secrets
- **No Data Retention**: Images processed in memory only
- **Secure Transmission**: End-to-end encryption

### Privacy Protection
- **Analytics Only**: Usage statistics without personal data
- **No Image Storage**: Images processed and discarded
- **Session Tracking**: Anonymous usage analytics
- **GDPR Compliance**: Privacy-first design

## 📈 Performance & Scalability

### Performance Features
- **Smart Caching**: Reduced API calls and faster responses
- **Fallback Systems**: High availability with multiple providers
- **Error Handling**: Graceful degradation and user feedback
- **Mobile Optimization**: Responsive design for all devices

### Scalability
- **Snowflake Cloud**: Auto-scaling compute resources
- **CDN Integration**: Cloudflare for global performance
- **Load Balancing**: Multiple Snowflake IP addresses
- **Database Optimization**: Efficient query performance

## 🛠️ Development & Testing

### Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/tweeterbot.git
cd tweeterbot

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

### Testing Suite
```bash
# Test domain setup
python test_domain.py

# Test Snowflake app
python test_snowflake_direct.py

# Test without SSL
python test_without_ssl.py

# Simple domain test
python simple_domain_test.py
```

## 📚 Documentation

### Setup Guides
- **SNOWFLAKE_PUBLIC_DEPLOYMENT.md**: Complete Snowflake deployment
- **CUSTOM_DOMAIN_SETUP.md**: Domain configuration guide
- **RAISEYOURVOICE_DOMAIN_SETUP.md**: Specific domain setup
- **GODADDY_DNS_FIX.md**: DNS troubleshooting
- **DOMAIN_TEST_RESULTS.md**: Testing and validation

### Configuration Files
- **domain_setup/**: Complete domain configuration
- **snowflake_deployment/**: Snowflake deployment package
- **requirements.txt**: Python dependencies
- **streamlit_app.py**: Main application file

## 🤝 Contributing

### How to Contribute
1. **Fork Repository**: Create your own fork
2. **Create Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Implement your improvements
4. **Test Thoroughly**: Ensure everything works
5. **Submit PR**: Create pull request with description

### Development Guidelines
- **Code Style**: Follow Python PEP 8
- **Documentation**: Update README and comments
- **Testing**: Test all new features
- **Compatibility**: Ensure Snowflake SiS compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Troubleshooting

### Getting Help
- **Documentation**: Check the guides in `/docs`
- **Issues**: Create GitHub issue for bugs
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact for direct support

### Common Issues
- **Domain Issues**: Check DNS configuration and Cloudflare setup
- **API Errors**: Verify API keys and quotas
- **Snowflake Issues**: Check app deployment and permissions
- **Performance**: Monitor usage and optimize

## 🎯 Roadmap

### Upcoming Features
- **Multi-language Support**: Support for multiple languages
- **Advanced Analytics**: Enhanced reporting and insights
- **API Integration**: REST API for external integrations
- **Mobile App**: Native mobile application
- **Team Collaboration**: Multi-user features and sharing

### Performance Improvements
- **Caching Layer**: Redis for improved performance
- **Image Optimization**: Advanced compression and processing
- **CDN Integration**: Enhanced global content delivery
- **Database Optimization**: Advanced query performance

---

**🌐 Live Application**: [https://raiseyourvoice.co.in](https://raiseyourvoice.co.in)

**📧 Contact**: For support and inquiries

**⭐ Star**: If you find this project helpful!

**🏗️ Architecture**: Professional deployment with custom domain and enterprise-grade infrastructure