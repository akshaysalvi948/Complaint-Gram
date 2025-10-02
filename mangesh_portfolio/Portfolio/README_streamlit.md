# Mangesh's Portfolio - Streamlit App

A modern, interactive portfolio website built with Streamlit that showcases certifications, work experience, and professional skills with dynamic visualizations and interactive features.

## 🚀 Features

- **Interactive Navigation**: Sidebar navigation with multiple sections
- **Dynamic Visualizations**: Charts and graphs using Plotly
- **Responsive Design**: Mobile-friendly layout
- **Interactive Elements**: Filters, forms, and expandable sections
- **Professional Styling**: Custom CSS with modern design
- **Real-time Data**: Interactive charts and metrics

## 📋 Sections

1. **Home**: Overview with quick stats and welcome message
2. **About**: Professional background with career timeline
3. **Certifications**: Interactive certification showcase with filters
4. **Work Experience**: Detailed work history with skill tags
5. **Skills**: Technical skills with proficiency charts
6. **Projects**: Featured projects with expandable details
7. **Contact**: Contact form and information

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Plotly**: Interactive charts and visualizations
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Custom CSS**: Professional styling and animations

## 📁 Project Structure

```
Portfolio/
│
├── portfolio_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── README_streamlit.md      # Streamlit-specific documentation
└── README.md               # General project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or Download** the repository:
   ```bash
   git clone <repository-url>
   # or download and extract the ZIP file
   ```

2. **Navigate** to the project directory:
   ```bash
   cd Portfolio
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   streamlit run portfolio_app.py
   ```

5. **Access the App**:
   - The app will automatically open in your browser
   - If not, navigate to `http://localhost:8501`

## 🎯 Usage

### Navigation
- Use the sidebar to navigate between different sections
- Each section offers unique interactive features

### Interactive Features
- **Filters**: Use dropdown menus to filter certifications and work experience
- **Charts**: Interactive charts with hover effects and zoom capabilities
- **Forms**: Contact form with validation
- **Expandable Sections**: Click to expand project details

### Customization
- Modify data in the Python file to update your information
- Adjust styling in the CSS section
- Add new sections by extending the navigation

## ✏️ Customization Guide

### Personal Information

1. **Update Contact Details** in `portfolio_app.py`:
   ```python
   # Update these variables
   certifications_data = [
       {
           "name": "Your Certification Name",
           "issuer": "Issuing Organization",
           "date": "2024",
           "description": "Your certification description",
           "icon": "🏆"
       }
   ]
   ```

2. **Modify Work Experience**:
   ```python
   work_experience = [
       {
           "title": "Your Job Title",
           "company": "Company Name",
           "period": "2023 - Present",
           "description": "Job description...",
           "skills": ["Skill1", "Skill2"],
           "duration": "1+ years"
       }
   ]
   ```

3. **Update Skills**:
   ```python
   skills_data = {
       "Your Category": ["Skill1", "Skill2", "Skill3"],
       "Another Category": ["Skill4", "Skill5"]
   }
   ```

### Styling

1. **Colors**: Update the CSS section in the app:
   ```python
   st.markdown("""
   <style>
       .main-header {
           background: linear-gradient(90deg, #your-color1, #your-color2);
       }
   </style>
   """, unsafe_allow_html=True)
   ```

2. **Theme**: Modify `.streamlit/config.toml`:
   ```toml
   [theme]
   primaryColor = "#your-primary-color"
   backgroundColor = "#your-background-color"
   ```

### Adding New Sections

1. **Add to Navigation**:
   ```python
   page = st.sidebar.selectbox(
       "Choose a section:",
       ["Home", "About", "New Section", "Contact"]
   )
   ```

2. **Create Section Logic**:
   ```python
   elif page == "New Section":
       st.markdown('<h1 class="section-header">New Section</h1>', unsafe_allow_html=True)
       # Your content here
   ```

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. **Push** your code to GitHub
2. **Go to** [share.streamlit.io](https://share.streamlit.io)
3. **Connect** your GitHub account
4. **Select** your repository and branch
5. **Deploy** with one click

### Heroku

1. **Create** a `Procfile`:
   ```
   web: streamlit run portfolio_app.py --server.port $PORT --server.headless true
   ```

2. **Deploy** using Heroku CLI:
   ```bash
   git add .
   git commit -m "Deploy Streamlit app"
   git push heroku main
   ```

### Docker

1. **Create** a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "portfolio_app.py", "--server.headless", "true"]
   ```

2. **Build and Run**:
   ```bash
   docker build -t portfolio-app .
   docker run -p 8501:8501 portfolio-app
   ```

## 📊 Data Structure

### Certifications
```python
{
    "name": "Certification Name",
    "issuer": "Issuing Organization",
    "date": "Year",
    "description": "Description",
    "icon": "Emoji Icon"
}
```

### Work Experience
```python
{
    "title": "Job Title",
    "company": "Company Name",
    "period": "Start - End",
    "description": "Job Description",
    "skills": ["Skill1", "Skill2"],
    "duration": "Duration"
}
```

## 🎨 Styling Features

- **Gradient Backgrounds**: Modern gradient effects
- **Card Layouts**: Professional card-based design
- **Interactive Elements**: Hover effects and animations
- **Responsive Design**: Mobile-friendly layout
- **Custom Components**: Styled buttons and forms

## 📱 Mobile Support

The app is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   streamlit run portfolio_app.py --server.port 8502
   ```

2. **Dependencies Issues**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **CSS Not Loading**:
   - Check that the CSS is properly formatted
   - Ensure no syntax errors in the markdown

### Performance Tips

- Use `st.cache_data` for expensive computations
- Optimize chart rendering for large datasets
- Consider pagination for large lists

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

For support and questions:
- Check the Streamlit documentation
- Review the code comments
- Test changes in development mode first

---

**Built with ❤️ using Streamlit**

*Last updated: December 2024*
