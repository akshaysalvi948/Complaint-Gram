import streamlit as st
import base64
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Akshay Salvi - Senior Data Engineer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern Danube Properties inspired styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%);
        color: white;
        padding: 4rem 2rem;
        text-align: center;
        border-radius: 20px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 400;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    .cta-button {
        background: linear-gradient(45deg, #f59e0b, #f97316);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.6);
    }
    
    /* Navigation */
    .nav-container {
        background: white;
        padding: 1rem 0;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .nav-button {
        background: transparent;
        border: 2px solid #e5e7eb;
        color: #374151;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-button:hover {
        background: #3b82f6;
        color: white;
        border-color: #3b82f6;
        transform: translateY(-1px);
    }
    
    .nav-button.active {
        background: #3b82f6;
        color: white;
        border-color: #3b82f6;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
        margin: 3rem 0 2rem 0;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
        border-radius: 2px;
    }
    
    /* Cards */
    .modern-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
        margin-bottom: 2rem;
    }
    
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .experience-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .experience-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .project-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid #f1f5f9;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .project-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    /* Skill Badges */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(45deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        margin: 0.5rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }
    
    .skill-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* Metrics Cards */
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(45deg, #10b981, #059669);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .metric-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    /* Feature Highlights */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Contact Section */
    .contact-info {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .sub-header {
            font-size: 1.2rem;
        }
        
        .hero-section {
            padding: 2rem 1rem;
        }
        
        .modern-card, .experience-card, .project-card {
            padding: 1.5rem;
        }
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Function to load and display profile image
def load_profile_image():
    """Load and display profile image with fallback to placeholder"""
    try:
        # Try to load actual profile image
        if os.path.exists("profile_photo.jpg"):
            st.image("profile_photo.jpg", width=200, use_container_width=False)
        elif os.path.exists("profile_placeholder.jpg"):
            st.image("profile_placeholder.jpg", width=200, use_container_width=False)
        else:
            # Fallback to CSS placeholder
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="width: 200px; height: 200px; border-radius: 50%; background-color: #3498db; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: white; font-size: 4rem;">
                    AS
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        # Fallback to CSS placeholder if image loading fails
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="width: 200px; height: 200px; border-radius: 50%; background-color: #3498db; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: white; font-size: 4rem;">
                AS
            </div>
        </div>
        """, unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="main-header">Akshay Salvi</h1>
        <p class="sub-header">Senior Data Engineer | Data Pipeline Architect | Cloud Solutions Expert</p>
        <p style="font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;">
            Transforming data into actionable insights with cutting-edge technology and innovative solutions
        </p>
        <a href="#about" class="cta-button">Explore My Work</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Load profile image in a modern card
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <div style="display: inline-block; padding: 1rem; background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
""", unsafe_allow_html=True)
load_profile_image()
st.markdown("</div></div>", unsafe_allow_html=True)

# Modern Navigation
st.markdown("""
<div class="nav-container">
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🏠 About", use_container_width=True, key="nav_about"):
        st.session_state.page = "about"
with col2:
    if st.button("💼 Experience", use_container_width=True, key="nav_experience"):
        st.session_state.page = "experience"
with col3:
    if st.button("🛠️ Skills", use_container_width=True, key="nav_skills"):
        st.session_state.page = "skills"
with col4:
    if st.button("🚀 Projects", use_container_width=True, key="nav_projects"):
        st.session_state.page = "projects"
with col5:
    if st.button("📞 Contact", use_container_width=True, key="nav_contact"):
        st.session_state.page = "contact"

st.markdown("</div></div>", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "about"

st.markdown("---")

# About Section
if st.session_state.page == "about":
    st.markdown('<h2 class="section-header">About Me</h2>', unsafe_allow_html=True)
    
    # Key metrics section
    st.markdown('<h3 style="text-align: center; color: #1e293b; margin-bottom: 2rem;">Key Achievements</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">7+</div>
            <p style="margin: 0; font-weight: 600; color: #64748b;">Years Experience</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">50+</div>
            <p style="margin: 0; font-weight: 600; color: #64748b;">Projects Delivered</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">15+</div>
            <p style="margin: 0; font-weight: 600; color: #64748b;">Technologies</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">5+</div>
            <p style="margin: 0; font-weight: 600; color: #64748b;">Cloud Platforms</p>
        </div>
        """, unsafe_allow_html=True)
    
    # About content
    st.markdown("""
    <div class="modern-card">
        <h3 style="color: #1e293b; margin-bottom: 1.5rem;">Professional Summary</h3>
        <div style="font-size: 1.1rem; line-height: 1.7; color: #475569;">
        <p>I am a Senior Data Engineer with 7+ years of experience in Data Engineering, 
        Compliance Automation, and Software Development. My expertise lies in building scalable ETL 
        pipelines, designing cloud-native solutions, and developing AI-driven compliance frameworks 
        that streamline processes and reduce manual effort.</p>
        
        <p>I have worked across diverse domains including Finance, Retail, and Food, delivering solutions that combine data integrity, 
        regulatory compliance, and automation.</p>
        
        <p>My expertise spans across cloud platforms (AWS, Azure, GCP), big data technologies (Spark, Hadoop, Kafka), 
        and modern data stack tools. I have a proven track record of leading data engineering teams and delivering 
        high-impact projects that improve data quality, reduce processing time, and enable real-time analytics.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    st.markdown('<h3 style="text-align: center; color: #1e293b; margin: 3rem 0 2rem 0;">Why Choose My Services?</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <h4 style="color: #1e293b; margin-bottom: 1rem;">Scalable Solutions</h4>
            <p style="color: #64748b;">Building enterprise-grade data pipelines that scale with your business needs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h4 style="color: #1e293b; margin-bottom: 1rem;">Fast Delivery</h4>
            <p style="color: #64748b;">Rapid development and deployment of data solutions with proven methodologies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h4 style="color: #1e293b; margin-bottom: 1rem;">AI-Powered</h4>
            <p style="color: #64748b;">Leveraging cutting-edge AI and ML technologies for intelligent automation</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Expertise areas
    st.markdown("""
    <div class="modern-card">
        <h3 style="color: #1e293b; margin-bottom: 1.5rem;">Key Expertise Areas</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
            <div>
                <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">🔹 Cloud & Data Platforms</h4>
                <p style="color: #64748b; margin: 0;">AWS (S3, Glue, Lambda, Redshift), Azure (Databricks, Synapse, Data Factory), GCP (BigQuery, Composer), Snowflake</p>
            </div>
            <div>
                <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">🔹 ETL & Data Engineering</h4>
                <p style="color: #64748b; margin: 0;">End-to-end pipelines, data validation, schema enforcement, deduplication, event-driven workflows</p>
            </div>
            <div>
                <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">🔹 Programming & Tools</h4>
                <p style="color: #64748b; margin: 0;">PySpark, Hive, Hadoop ecosystem, Pandas, Flask (REST APIs), SQLAlchemy, Psycopg, Boto3</p>
            </div>
            <div>
                <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">🔹 Compliance & Automation</h4>
                <p style="color: #64748b; margin: 0;">Regulatory monitoring, validation systems, audit trails, metadata catalogs</p>
            </div>
            <div>
                <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">🔹 AI & GenAI Applications</h4>
                <p style="color: #64748b; margin: 0;">Risk analysis, audit support, policy summarization, anomaly detection, predictive compliance analytics, multi-agent LLM frameworks</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Experience Section
elif st.session_state.page == "experience":
    st.markdown('<h2 class="section-header">Professional Experience</h2>', unsafe_allow_html=True)
    
    # Experience timeline
    experiences = [
        {
            "title": "Senior Compliance Data Engineer",
            "company": "Avalara",
            "duration": "2025 Jan - Present",
            "description": [
                "1. Developing tools to enhance efficiency and accuracy in compliance processes",
                "Designing intelligent compliance monitoring tools that automatically track regulatory changes and update internal compliance frameworks",
                "Creating automated validation systems that check data against regulatory standards, ensuring fewer manual errors.",
                "Implementing workflow automation that accelerates approval processes, audit readiness, and reporting timelines",
                "Leveraging cloud-native platforms (Snowflake, AWS, and other AI tools) with inbuilt governance to safeguard sensitive information.",
                "Utilizing AI tools to reduce manual efforts and repetitive tasks",
                "Building GenAI agents using different LLMs and implementing multi-agent AI frameworks to improve efficiency and outcomes",
                "Mentored junior engineers and established best practices for code review and documentation"
            ]
        },
        {
            "title": "Senior Data Engineer",
            "company": "Bizmetric",
            "duration": "Feb 2021 - Jan 2025",
            "description": [
                "Worked with different technologies such as ETL Data Modeling, Data Extraction, Data Cleaning, Data Processing, and creating Data pipelines",
                "Used cloud services including AWS (S3, Lambda, Glue, Workflow, Secret Manager, SNS, Redshift database)",
                "Implemented Azure solutions (Databricks, Synapse, Data Factory, Key Vault, SQL Server, Container App, Registry, Kubernetes)",
                "Developed GCP solutions (BigQuery, Composer/Airflow) for data processing and orchestration",
                "Built scalable data pipelines processing 5TB+ of data daily using Python and Apache Airflow",
                "Optimized SQL queries and data warehouse performance, improving query speed by 60%"
            ]
        },
        {
            "title": "Junior Data Scientist",
            "company": "KayaDev AI ",
            "duration": "Jun 2018 - Feb 2021",
            "description": [
                "Developed data pipelines using Python, SQL, and Apache Spark",
                "Created automated data validation and quality checks",
                "Assisted in building data warehouses and data lakes",
                "Participated in agile development processes and code reviews",
                "Gained experience with various database technologies (PostgreSQL, MongoDB, Redis)"
            ]
        }
    ]
    
    for exp in experiences:
        st.markdown(f"""
        <div class="experience-card">
            <h3 style="color: #2c3e50; margin-top: 0;">{exp['title']}</h3>
            <h4 style="color: #3498db; margin: 0.5rem 0;">{exp['company']}</h4>
            <p style="color: #666; font-style: italic; margin: 0.5rem 0;">{exp['duration']}</p>
            <ul style="margin: 1rem 0;">
        """, unsafe_allow_html=True)
        
        for desc in exp['description']:
            st.markdown(f"<li>{desc}</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)

# Skills Section
elif st.session_state.page == "skills":
    st.markdown('<h2 class="section-header">Technical Skills</h2>', unsafe_allow_html=True)
    
    # Skills categories
    skills_data = {
        "Programming Languages": ["Python", "SQL", "Scala", "Java", "R", "Bash"],
        "Big Data Technologies": ["Apache Spark", "Apache Kafka", "Apache Airflow", "Hadoop", "Hive", "Presto"],
        "Cloud Platforms": ["AWS", "Azure", "Google Cloud Platform", "Databricks", "Snowflake"],
        "Databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "DynamoDB"],
        "Data Tools": ["dbt", "Great Expectations", "Apache Superset", "Tableau", "Power BI"],
        "DevOps & CI/CD": ["Docker", "Kubernetes", "Jenkins", "Git", "Terraform", "Ansible"]
    }
    
    # Create skill visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        for category, skills in skills_data.items():
            st.markdown(f"<h4 style='color: #2c3e50; margin-top: 1.5rem;'>{category}</h4>", unsafe_allow_html=True)
            skill_html = ""
            for skill in skills:
                skill_html += f'<span class="skill-badge">{skill}</span>'
            st.markdown(skill_html, unsafe_allow_html=True)
    
    with col2:
        # Skills proficiency chart
        st.markdown('<h4 style="color: #2c3e50;">Skills Proficiency</h4>', unsafe_allow_html=True)
        
        proficiency_data = {
            'Skill': ['Python', 'SQL', 'Apache Spark', 'AWS', 'Apache Kafka', 'Docker', 'Apache Airflow', 'PostgreSQL'],
            'Proficiency': [95, 90, 85, 80, 75, 70, 85, 80]
        }
        
        df = pd.DataFrame(proficiency_data)
        fig = px.bar(df, x='Proficiency', y='Skill', orientation='h', 
                    color='Proficiency', color_continuous_scale='Blues')
        fig.update_layout(height=400, showlegend=False, 
                         plot_bgcolor='rgba(0,0,0,0)', 
                         paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# Projects Section
elif st.session_state.page == "projects":
    st.markdown('<h2 class="section-header">Featured Projects</h2>', unsafe_allow_html=True)
    
    # Project showcase header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h3 style="color: #1e293b; font-size: 1.5rem; margin-bottom: 1rem;">Innovative Data Solutions</h3>
        <p style="color: #64748b; font-size: 1.1rem;">Transforming complex data challenges into scalable, intelligent solutions</p>
    </div>
    """, unsafe_allow_html=True)
    
    projects = [
        {
            "title": "Real-Time Analytics Platform",
            "description": "Built a comprehensive real-time analytics platform processing 1M+ events per second using Apache Kafka, Apache Spark Streaming, and Apache Druid.",
            "technologies": ["Apache Kafka", "Apache Spark", "Apache Druid", "Python", "AWS", "Docker"],
            "impact": "Reduced data processing latency by 80% and enabled real-time business insights",
            "category": "Real-Time Processing",
            "icon": "⚡"
        },
        {
            "title": "Data Lake Migration & Modernization",
            "description": "Led the migration of legacy data warehouse to modern cloud data lake architecture on AWS, implementing data governance and quality frameworks.",
            "technologies": ["AWS S3", "Apache Spark", "dbt", "Great Expectations", "Apache Airflow", "Terraform"],
            "impact": "Reduced infrastructure costs by 50% and improved data accessibility across the organization",
            "category": "Cloud Migration",
            "icon": "☁️"
        },
        {
            "title": "ML Pipeline Automation",
            "description": "Designed and implemented automated ML pipeline for model training, validation, and deployment using MLOps best practices.",
            "technologies": ["Python", "Apache Airflow", "Docker", "Kubernetes", "MLflow", "AWS SageMaker"],
            "impact": "Reduced model deployment time from weeks to hours and improved model accuracy by 15%",
            "category": "Machine Learning",
            "icon": "🤖"
        },
        {
            "title": "Data Quality Monitoring System",
            "description": "Developed a comprehensive data quality monitoring system with automated alerting and data lineage tracking.",
            "technologies": ["Python", "Great Expectations", "Apache Airflow", "PostgreSQL", "Grafana"],
            "impact": "Improved data quality by 90% and reduced data-related incidents by 70%",
            "category": "Data Quality",
            "icon": "📊"
        }
    ]
    
    # Display projects in a grid layout
    for i in range(0, len(projects), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(projects):
                project = projects[i]
                st.markdown(f"""
                <div class="project-card">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 2rem; margin-right: 1rem;">{project['icon']}</span>
                        <div>
                            <h3 style="color: #1e293b; margin: 0; font-size: 1.3rem;">{project['title']}</h3>
                            <span style="background: linear-gradient(45deg, #3b82f6, #8b5cf6); color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem; font-weight: 500;">{project['category']}</span>
                        </div>
                    </div>
                    <p style="color: #64748b; line-height: 1.6; margin: 1rem 0;">{project['description']}</p>
                    <div style="margin: 1.5rem 0;">
                        <h4 style="color: #3b82f6; margin-bottom: 0.5rem; font-size: 1rem;">Technologies:</h4>
                """, unsafe_allow_html=True)
                
                tech_html = ""
                for tech in project['technologies']:
                    tech_html += f'<span class="skill-badge" style="font-size: 0.8rem; padding: 0.5rem 1rem;">{tech}</span>'
                st.markdown(tech_html, unsafe_allow_html=True)
                
                st.markdown(f"""
                    </div>
                    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 1rem; border-radius: 10px; border-left: 4px solid #10b981;">
                        <h4 style="color: #059669; margin: 0 0 0.5rem 0; font-size: 1rem;">Impact:</h4>
                        <p style="color: #047857; margin: 0; font-weight: 500;">{project['impact']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if i + 1 < len(projects):
                project = projects[i + 1]
                st.markdown(f"""
                <div class="project-card">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 2rem; margin-right: 1rem;">{project['icon']}</span>
                        <div>
                            <h3 style="color: #1e293b; margin: 0; font-size: 1.3rem;">{project['title']}</h3>
                            <span style="background: linear-gradient(45deg, #3b82f6, #8b5cf6); color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem; font-weight: 500;">{project['category']}</span>
                        </div>
                    </div>
                    <p style="color: #64748b; line-height: 1.6; margin: 1rem 0;">{project['description']}</p>
                    <div style="margin: 1.5rem 0;">
                        <h4 style="color: #3b82f6; margin-bottom: 0.5rem; font-size: 1rem;">Technologies:</h4>
                """, unsafe_allow_html=True)
                
                tech_html = ""
                for tech in project['technologies']:
                    tech_html += f'<span class="skill-badge" style="font-size: 0.8rem; padding: 0.5rem 1rem;">{tech}</span>'
                st.markdown(tech_html, unsafe_allow_html=True)
                
                st.markdown(f"""
                    </div>
                    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 1rem; border-radius: 10px; border-left: 4px solid #10b981;">
                        <h4 style="color: #059669; margin: 0 0 0.5rem 0; font-size: 1rem;">Impact:</h4>
                        <p style="color: #047857; margin: 0; font-weight: 500;">{project['impact']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Project statistics
    st.markdown("""
    <div class="modern-card" style="margin-top: 3rem;">
        <h3 style="color: #1e293b; text-align: center; margin-bottom: 2rem;">Project Impact Summary</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem;">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 800; color: #3b82f6; margin-bottom: 0.5rem;">80%</div>
                <p style="color: #64748b; margin: 0;">Latency Reduction</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 800; color: #10b981; margin-bottom: 0.5rem;">50%</div>
                <p style="color: #64748b; margin: 0;">Cost Savings</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 800; color: #f59e0b; margin-bottom: 0.5rem;">90%</div>
                <p style="color: #64748b; margin: 0;">Quality Improvement</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 800; color: #8b5cf6; margin-bottom: 0.5rem;">15%</div>
                <p style="color: #64748b; margin: 0;">Accuracy Boost</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Contact Section
elif st.session_state.page == "contact":
    st.markdown('<h2 class="section-header">Get In Touch</h2>', unsafe_allow_html=True)
    
    # Contact header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h3 style="color: #1e293b; font-size: 1.5rem; margin-bottom: 1rem;">Let's Build Something Amazing Together</h3>
        <p style="color: #64748b; font-size: 1.1rem;">Ready to transform your data challenges into innovative solutions? Let's connect!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Contact information cards
        st.markdown("""
        <div class="modern-card">
            <h3 style="color: #1e293b; margin-bottom: 1.5rem; text-align: center;">Contact Information</h3>
        """, unsafe_allow_html=True)
        
        # Contact details with icons
        contact_details = [
            {"icon": "📧", "label": "Email", "value": "akshay.salvi@email.com", "link": "mailto:akshay.salvi@email.com"},
            {"icon": "📱", "label": "Phone", "value": "+91 7208974398", "link": "tel:+917208974398"},
            {"icon": "📍", "label": "Location", "value": "Mumbai, India", "link": None},
            {"icon": "💼", "label": "LinkedIn", "value": "linkedin.com/in/akshay-salvi-2869b2125/", "link": "https://www.linkedin.com/in/akshay-salvi-2869b2125/"},
            {"icon": "🐙", "label": "GitHub", "value": "github.com/akshaysalvi", "link": "https://github.com/akshaysalvi"}
        ]
        
        for detail in contact_details:
            if detail["link"]:
                st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 1rem; padding: 1rem; background: #f8fafc; border-radius: 10px; transition: all 0.3s ease;" onmouseover="this.style.background='#e2e8f0'" onmouseout="this.style.background='#f8fafc'">
                    <span style="font-size: 1.5rem; margin-right: 1rem;">{detail['icon']}</span>
                    <div>
                        <h4 style="color: #1e293b; margin: 0; font-size: 0.9rem; font-weight: 600;">{detail['label']}</h4>
                        <a href="{detail['link']}" style="color: #3b82f6; text-decoration: none; font-weight: 500;">{detail['value']}</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 1rem; padding: 1rem; background: #f8fafc; border-radius: 10px;">
                    <span style="font-size: 1.5rem; margin-right: 1rem;">{detail['icon']}</span>
                    <div>
                        <h4 style="color: #1e293b; margin: 0; font-size: 0.9rem; font-weight: 600;">{detail['label']}</h4>
                        <p style="color: #64748b; margin: 0; font-weight: 500;">{detail['value']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Availability info
        st.markdown("""
        <div class="modern-card">
            <h3 style="color: #1e293b; margin-bottom: 1rem; text-align: center;">Availability</h3>
            <div style="text-align: center;">
                <div style="display: inline-block; background: linear-gradient(45deg, #10b981, #059669); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; margin-bottom: 1rem;">
                    🟢 Available for Projects
                </div>
                <p style="color: #64748b; margin: 0;">Response time: Usually within 24 hours</p>
                <p style="color: #64748b; margin: 0.5rem 0 0 0;">Available for freelance projects and full-time opportunities</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Contact form
        st.markdown("""
        <div class="modern-card">
            <h3 style="color: #1e293b; margin-bottom: 1.5rem; text-align: center;">Send a Message</h3>
        """, unsafe_allow_html=True)
        
        with st.form("contact_form"):
            name = st.text_input("👤 Your Name", placeholder="Enter your full name")
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            subject = st.text_input("📝 Subject", placeholder="What's this about?")
            message = st.text_area("💬 Message", height=150, placeholder="Tell me about your project or how I can help...")
            submit_button = st.form_submit_button("🚀 Send Message", use_container_width=True)
            
            if submit_button:
                if name and email and subject and message:
                    st.success("✅ Thank you for your message! I'll get back to you soon.")
                else:
                    st.error("❌ Please fill in all fields.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Call to action section
    st.markdown("""
    <div class="hero-section" style="margin-top: 3rem; padding: 3rem 2rem;">
        <div class="hero-content">
            <h3 style="font-size: 2rem; margin-bottom: 1rem;">Ready to Start Your Next Project?</h3>
            <p style="font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;">
                Let's discuss how we can transform your data challenges into innovative solutions
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="mailto:akshay.salvi@email.com" class="cta-button">📧 Email Me</a>
                <a href="https://www.linkedin.com/in/akshay-salvi-2869b2125/" class="cta-button" style="background: linear-gradient(45deg, #0077b5, #005885);">💼 LinkedIn</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Modern Footer
st.markdown("""
<div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white; padding: 3rem 2rem; margin-top: 3rem; border-radius: 20px 20px 0 0;">
    <div style="text-align: center;">
        <h3 style="color: white; margin-bottom: 1rem; font-size: 1.5rem;">Akshay Salvi</h3>
        <p style="color: #cbd5e1; margin-bottom: 2rem; font-size: 1.1rem;">Senior Data Engineer | Transforming Data into Insights</p>
        
        <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 2rem; flex-wrap: wrap;">
            <a href="mailto:akshay.salvi@email.com" style="color: #60a5fa; text-decoration: none; font-weight: 500;">📧 Email</a>
            <a href="https://www.linkedin.com/in/akshay-salvi-2869b2125/" style="color: #60a5fa; text-decoration: none; font-weight: 500;">💼 LinkedIn</a>
            <a href="https://github.com/akshaysalvi" style="color: #60a5fa; text-decoration: none; font-weight: 500;">🐙 GitHub</a>
        </div>
        
        <div style="border-top: 1px solid #475569; padding-top: 2rem;">
            <p style="color: #94a3b8; margin: 0;">&copy; 2024 Akshay Salvi. Built with ❤️ using Streamlit</p>
            <p style="color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Available for freelance projects and full-time opportunities</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
