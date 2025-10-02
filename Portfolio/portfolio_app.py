import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="Mangesh's Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2563eb;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #2563eb;
        padding-bottom: 0.5rem;
    }
    
    .cert-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .work-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #2563eb;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .skill-tag {
        background: #2563eb;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.9rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    .contact-info {
        background: #f1f5f9;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #2563eb);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Data for the portfolio
certifications_data = [
    {
        "name": "Snowflake Data Engineer",
        "issuer": "Snowflake Inc.",
        "date": "2024",
        "description": "Advanced certification in Snowflake data warehousing, ETL processes, and analytics solutions.",
        "icon": "❄️"
    },
    {
        "name": "AWS Cloud Practitioner",
        "issuer": "Amazon Web Services",
        "date": "2023",
        "description": "Fundamental understanding of AWS Cloud concepts, services, and architectural best practices.",
        "icon": "☁️"
    },
    {
        "name": "SQL Database Specialist",
        "issuer": "Microsoft",
        "date": "2023",
        "description": "Advanced SQL programming, database optimization, and performance tuning expertise.",
        "icon": "🗄️"
    },
    {
        "name": "Python Programming",
        "issuer": "Python Institute",
        "date": "2022",
        "description": "Comprehensive Python development skills including data analysis, automation, and web development.",
        "icon": "🐍"
    },
    {
        "name": "Data Analytics Professional",
        "issuer": "Google",
        "date": "2022",
        "description": "Data analysis, visualization, and business intelligence using modern analytics tools.",
        "icon": "📊"
    }
]

work_experience = [
    {
        "title": "Data Engineer",
        "company": "Tech Solutions Inc.",
        "period": "2023 - Present",
        "description": "Designing and implementing data pipelines using Snowflake, optimizing data warehouse performance, and collaborating with cross-functional teams to deliver data-driven solutions.",
        "skills": ["Snowflake", "SQL", "Python", "ETL Processes", "Data Modeling"],
        "duration": "1+ years"
    },
    {
        "title": "Junior Data Analyst",
        "company": "Analytics Corp",
        "period": "2022 - 2023",
        "description": "Analyzed large datasets to provide business insights, created automated reports, and supported decision-making processes through data visualization and statistical analysis.",
        "skills": ["Data Analysis", "Tableau", "Excel", "Statistics", "Report Automation"],
        "duration": "1 year"
    },
    {
        "title": "Technical Support Specialist",
        "company": "IT Services Ltd.",
        "period": "2021 - 2022",
        "description": "Provided technical support to clients, resolved complex technical issues, and maintained documentation for troubleshooting procedures.",
        "skills": ["Technical Support", "Problem Solving", "Documentation", "Customer Service"],
        "duration": "1 year"
    }
]

skills_data = {
    "Data & Analytics": ["Snowflake", "SQL", "Python", "R", "Tableau", "Power BI", "Pandas", "NumPy"],
    "Cloud & Infrastructure": ["AWS", "Azure", "Docker", "Kubernetes", "Linux", "Git"],
    "Programming": ["Python", "JavaScript", "Java", "HTML/CSS", "GitHub"],
    "Tools & Technologies": ["Jupyter", "VS Code", "Postman", "Slack", "Confluence", "JIRA"]
}

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a section:",
    ["Home", "About", "Certifications", "Work Experience", "Skills", "Projects", "Contact"]
)

# Helper functions
def display_certification_card(cert):
    st.markdown(f"""
    <div class="cert-card">
        <h3>{cert['icon']} {cert['name']}</h3>
        <p><strong>Issuer:</strong> {cert['issuer']} | <strong>Date:</strong> {cert['date']}</p>
        <p>{cert['description']}</p>
    </div>
    """, unsafe_allow_html=True)

def display_work_card(work):
    skills_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in work['skills']])
    st.markdown(f"""
    <div class="work-card">
        <h3>{work['title']} at {work['company']}</h3>
        <p><strong>Period:</strong> {work['period']} ({work['duration']})</p>
        <p>{work['description']}</p>
        <div style="margin-top: 1rem;">
            <strong>Key Skills:</strong><br>
            {skills_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content based on selected page
if page == "Home":
    st.markdown('<h1 class="main-header">Hi, I\'m Mangesh</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>5+</h2>
            <p>Professional Certifications</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>2+</h2>
            <p>Years Experience</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>10+</h2>
            <p>Projects Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    ## Welcome to My Portfolio! 🚀
    
    I'm a dedicated professional with expertise in data engineering, cloud technologies, and continuous learning. 
    My journey in technology has been marked by a commitment to excellence and staying current with industry best practices.
    
    ### What You'll Find Here:
    - 📜 **Certifications**: My professional achievements and credentials
    - 💼 **Work Experience**: Timeline of my career progression
    - 🛠️ **Skills**: Technical and professional competencies
    - 📊 **Projects**: Interactive demonstrations of my work
    - 📞 **Contact**: Ways to get in touch with me
    
    Use the sidebar to navigate through different sections of my portfolio!
    """)
    
    # Interactive elements
    st.markdown("### Quick Stats")
    
    # Create a simple chart
    chart_data = pd.DataFrame({
        'Category': ['Data & Analytics', 'Cloud & Infrastructure', 'Programming', 'Tools & Technologies'],
        'Skills Count': [8, 6, 5, 6]
    })
    
    fig = px.bar(chart_data, x='Category', y='Skills Count', 
                 title="Skills Distribution by Category",
                 color='Skills Count',
                 color_continuous_scale='Blues')
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

elif page == "About":
    st.markdown('<h1 class="section-header">About Me</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Professional Background
        
        I am a passionate data engineer with a strong foundation in cloud technologies and data analytics. 
        My expertise spans across modern data platforms, with a particular focus on Snowflake and AWS ecosystems.
        
        ### Key Strengths:
        - **Data Engineering**: Building scalable data pipelines and warehouses
        - **Cloud Platforms**: AWS and Azure implementation and optimization
        - **Analytics**: Transforming raw data into actionable business insights
        - **Problem Solving**: Analytical approach to complex technical challenges
        - **Continuous Learning**: Committed to staying updated with latest technologies
        
        ### Professional Philosophy:
        I believe in the power of data to drive business decisions and create value. 
        My approach combines technical excellence with business acumen to deliver 
        solutions that not only work technically but also provide real business impact.
        """)
    
    with col2:
        # Interactive timeline
        timeline_data = pd.DataFrame({
            'Year': [2021, 2022, 2023, 2024],
            'Milestone': ['Started Career', 'Data Analytics Cert', 'AWS Cert', 'Snowflake Cert'],
            'Description': ['Technical Support', 'Python & Analytics', 'Cloud Practitioner', 'Data Engineer']
        })
        
        fig = go.Figure(data=go.Scatter(
            x=timeline_data['Year'],
            y=timeline_data['Milestone'],
            mode='markers+lines+text',
            text=timeline_data['Description'],
            textposition="top center",
            marker=dict(size=15, color='#2563eb'),
            line=dict(color='#2563eb', width=3)
        ))
        
        fig.update_layout(
            title="Career Timeline",
            xaxis_title="Year",
            yaxis_title="Milestones",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

elif page == "Certifications":
    st.markdown('<h1 class="section-header">Professional Certifications</h1>', unsafe_allow_html=True)
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    
    with col2:
        year_filter = st.selectbox("Filter by Year:", ["All"] + list(set([cert['date'] for cert in certifications_data])))
    
    # Display certifications
    filtered_certs = certifications_data
    if year_filter != "All":
        filtered_certs = [cert for cert in certifications_data if cert['date'] == year_filter]
    
    for cert in filtered_certs:
        display_certification_card(cert)
    
    # Certification timeline
    st.markdown("### Certification Timeline")
    cert_df = pd.DataFrame(certifications_data)
    cert_df['date'] = pd.to_datetime(cert_df['date'], format='%Y')
    
    fig = px.timeline(cert_df, x_start='date', x_end='date', y='name',
                      title="Certification Achievement Timeline",
                      color='name',
                      height=400)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

elif page == "Work Experience":
    st.markdown('<h1 class="section-header">Work Experience</h1>', unsafe_allow_html=True)
    
    # Experience filter
    col1, col2 = st.columns([3, 1])
    
    with col2:
        company_filter = st.selectbox("Filter by Company:", ["All"] + list(set([work['company'] for work in work_experience])))
    
    # Display work experience
    filtered_work = work_experience
    if company_filter != "All":
        filtered_work = [work for work in work_experience if work['company'] == company_filter]
    
    for work in filtered_work:
        display_work_card(work)
    
    # Skills progression chart
    st.markdown("### Skills Development Over Time")
    
    skills_progression = pd.DataFrame({
        'Year': [2021, 2022, 2023, 2024],
        'Technical Skills': [5, 8, 12, 18],
        'Certifications': [0, 2, 3, 5],
        'Projects': [2, 5, 8, 12]
    })
    
    fig = px.line(skills_progression, x='Year', y=['Technical Skills', 'Certifications', 'Projects'],
                  title="Professional Growth Metrics",
                  markers=True)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

elif page == "Skills":
    st.markdown('<h1 class="section-header">Technical Skills</h1>', unsafe_allow_html=True)
    
    # Skills visualization
    for category, skills in skills_data.items():
        st.markdown(f"### {category}")
        
        # Create skill tags
        skills_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in skills])
        st.markdown(f"<div style='margin: 1rem 0;'>{skills_html}</div>", unsafe_allow_html=True)
    
    # Skills proficiency chart
    st.markdown("### Skills Proficiency Levels")
    
    proficiency_data = pd.DataFrame({
        'Skill': ['Snowflake', 'SQL', 'Python', 'AWS', 'Tableau', 'Docker', 'Git'],
        'Proficiency': [90, 85, 80, 75, 70, 65, 60]
    })
    
    fig = px.bar(proficiency_data, x='Proficiency', y='Skill', orientation='h',
                 title="Skills Proficiency Assessment",
                 color='Proficiency',
                 color_continuous_scale='Blues')
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

elif page == "Projects":
    st.markdown('<h1 class="section-header">Featured Projects</h1>', unsafe_allow_html=True)
    
    # Project showcase
    projects = [
        {
            "name": "Data Pipeline Automation",
            "description": "Automated ETL pipeline using Snowflake and Python for real-time data processing",
            "tech_stack": ["Snowflake", "Python", "AWS", "Airflow"],
            "status": "Completed"
        },
        {
            "name": "Business Intelligence Dashboard",
            "description": "Interactive dashboard for sales analytics using Tableau and SQL",
            "tech_stack": ["Tableau", "SQL", "PostgreSQL", "Python"],
            "status": "Completed"
        },
        {
            "name": "Cloud Migration Project",
            "description": "Migrated on-premise data warehouse to AWS cloud infrastructure",
            "tech_stack": ["AWS", "Snowflake", "Python", "Terraform"],
            "status": "In Progress"
        }
    ]
    
    for project in projects:
        with st.expander(f"🚀 {project['name']} - {project['status']}"):
            st.markdown(f"**Description:** {project['description']}")
            st.markdown(f"**Tech Stack:** {', '.join(project['tech_stack'])}")
            
            if st.button(f"View Details", key=f"project_{project['name']}"):
                st.success(f"Detailed information about {project['name']} would be displayed here!")

elif page == "Contact":
    st.markdown('<h1 class="section-header">Get In Touch</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="contact-info">
            <h3>Contact Information</h3>
            <p>📧 <strong>Email:</strong> mangesh.email@example.com</p>
            <p>📱 <strong>Phone:</strong> +1 (555) 123-4567</p>
            <p>📍 <strong>Location:</strong> Your City, Country</p>
            <p>💼 <strong>LinkedIn:</strong> linkedin.com/in/mangesh</p>
            <p>🐙 <strong>GitHub:</strong> github.com/mangesh</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Send me a message!")
        
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            subject = st.text_input("Subject")
            message = st.text_area("Message")
            submit_button = st.form_submit_button("Send Message")
            
            if submit_button:
                if name and email and subject and message:
                    st.success("Thank you for your message! I'll get back to you soon.")
                else:
                    st.error("Please fill in all fields.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; margin-top: 2rem;">
    <p>© 2024 Mangesh's Portfolio. Built with ❤️ using Streamlit</p>
    <p>Last updated: December 2024</p>
</div>
""", unsafe_allow_html=True)
