# Akshay Salvi - Senior Data Engineer Portfolio

A modern, interactive portfolio website built with Streamlit showcasing professional experience, skills, and projects as a Senior Data Engineer.

## 🚀 Features

- **Modern UI Design**: Clean, professional interface with responsive design
- **Interactive Navigation**: Easy-to-use navigation between different sections
- **Comprehensive Sections**:
  - About Me with key metrics
  - Professional Experience timeline
  - Technical Skills with proficiency visualization
  - Featured Projects with impact metrics
  - Contact form and information
- **Data Visualizations**: Interactive charts using Plotly
- **Mobile Responsive**: Works seamlessly on all devices
- **Easy Deployment**: Ready for Streamlit Community Cloud deployment

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Styling**: Custom CSS
- **Deployment**: Streamlit Community Cloud

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager

## 🚀 Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/personal-website.git
cd personal-website
```

### 2. Create Virtual Environment

```bash
python -m venv portfolio_env

# On Windows
portfolio_env\Scripts\activate

# On macOS/Linux
source portfolio_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run portfolio_app.py
```

The application will be available at `http://localhost:8501`

## 🌐 Deployment to Streamlit Community Cloud

### 1. Push to GitHub

```bash
git add .
git commit -m "Initial portfolio commit"
git push origin main
```

### 2. Deploy on Streamlit Community Cloud

1. Go to [Streamlit Community Cloud](https://share.streamlit.io/)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `yourusername/personal-website`
5. Set the main file path: `portfolio_app.py`
6. Click "Deploy"

Your portfolio will be live at: `https://yourusername-personal-website.streamlit.app/`

## 📁 Project Structure

```
personal-website/
├── portfolio_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
└── .streamlit/              # Streamlit configuration (optional)
    └── config.toml          # Custom configuration
```

## 🎨 Customization

### Adding Your Photo

1. Add your profile photo to the project directory
2. Update the `load_profile_image()` function in `portfolio_app.py`:

```python
def load_profile_image():
    st.image("path/to/your/photo.jpg", width=200, use_column_width=False)
```

### Updating Personal Information

Edit the following sections in `portfolio_app.py`:
- Personal details in the header
- Experience data in the `experiences` list
- Skills in the `skills_data` dictionary
- Projects in the `projects` list
- Contact information in the contact section

### Styling Customization

Modify the CSS in the `st.markdown()` section at the beginning of the file to customize colors, fonts, and layout.

## 📊 Portfolio Sections

### About Me
- Professional summary
- Key metrics and achievements
- Personal branding

### Experience
- Detailed work history
- Role descriptions and achievements
- Timeline format

### Skills
- Technical skills organized by category
- Interactive proficiency charts
- Technology badges

### Projects
- Featured project showcases
- Technology stacks used
- Impact and results

### Contact
- Contact form
- Professional links
- Availability information

## 🔧 Configuration

### Streamlit Configuration

Create a `.streamlit/config.toml` file for custom configuration:

```toml
[theme]
primaryColor = "#3498db"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#2c3e50"

[server]
port = 8501
enableCORS = false
```

## 📈 Analytics and Monitoring

Consider adding:
- Google Analytics integration
- Streamlit analytics
- Performance monitoring
- User feedback collection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

For questions or support, please contact:
- Email: akshay.salvi@email.com
- LinkedIn: [Akshay Salvi](https://www.linkedin.com/in/akshay-salvi-2869b2125/)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Icons from [Streamlit Icons](https://streamlit.io/)
- Styling inspired by modern web design principles

---

**Built with ❤️ by Akshay Salvi**