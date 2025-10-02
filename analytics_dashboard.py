"""
Analytics Dashboard for TweeterBot
Provides insights and visualizations of usage data stored in Snowflake
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from snowflake_manager import snowflake_manager

def show_analytics_dashboard():
    """Display the analytics dashboard"""
    st.title("📊 TweeterBot Analytics Dashboard")
    
    # Check Snowflake connection
    if not st.session_state.get('snowflake_connected', False):
        st.error("❌ Snowflake not connected. Analytics require database connection.")
        st.info("💡 Configure Snowflake credentials in the main app to view analytics.")
        return
    
    # Sidebar filters
    with st.sidebar:
        st.header("📊 Analytics Filters")
        
        # Date range selector
        date_range = st.selectbox(
            "Time Period",
            ["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
            index=1
        )
        
        # Convert to days
        days_map = {
            "Last 7 days": 7,
            "Last 30 days": 30,
            "Last 90 days": 90,
            "All time": 365  # Max 1 year for performance
        }
        days = days_map[date_range]
        
        # Refresh button
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
    
    # Main dashboard content
    col1, col2, col3, col4 = st.columns(4)
    
    # Get usage statistics
    try:
        usage_stats = snowflake_manager.get_daily_usage_stats(days)
        ai_performance = snowflake_manager.get_ai_provider_performance()
        recent_content = snowflake_manager.get_recent_content(50)
        
        if not usage_stats.empty:
            # Calculate summary metrics
            total_images = usage_stats['IMAGE_UPLOADS'].sum()
            total_generations = usage_stats['AI_GENERATIONS'].sum()
            total_tweets = usage_stats['TWEET_POSTS'].sum()
            success_rate = (usage_stats['SUCCESSFUL_EVENTS'].sum() / usage_stats['TOTAL_EVENTS'].sum() * 100) if usage_stats['TOTAL_EVENTS'].sum() > 0 else 0
            
            # Display key metrics
            with col1:
                st.metric(
                    label="📸 Images Uploaded",
                    value=f"{total_images:,}",
                    delta=f"+{usage_stats.iloc[0]['IMAGE_UPLOADS'] if len(usage_stats) > 0 else 0}" if len(usage_stats) > 1 else None
                )
            
            with col2:
                st.metric(
                    label="🤖 AI Generations",
                    value=f"{total_generations:,}",
                    delta=f"+{usage_stats.iloc[0]['AI_GENERATIONS'] if len(usage_stats) > 0 else 0}" if len(usage_stats) > 1 else None
                )
            
            with col3:
                st.metric(
                    label="🐦 Tweets Posted",
                    value=f"{total_tweets:,}",
                    delta=f"+{usage_stats.iloc[0]['TWEET_POSTS'] if len(usage_stats) > 0 else 0}" if len(usage_stats) > 1 else None
                )
            
            with col4:
                st.metric(
                    label="✅ Success Rate",
                    value=f"{success_rate:.1f}%",
                    delta=None
                )
            
            st.divider()
            
            # Usage trends chart
            st.subheader("📈 Usage Trends")
            
            if len(usage_stats) > 1:
                fig_trends = px.line(
                    usage_stats,
                    x='USAGE_DATE',
                    y=['IMAGE_UPLOADS', 'AI_GENERATIONS', 'TWEET_POSTS'],
                    title=f"Daily Usage Trends ({date_range})",
                    labels={'value': 'Count', 'USAGE_DATE': 'Date'},
                    color_discrete_map={
                        'IMAGE_UPLOADS': '#1f77b4',
                        'AI_GENERATIONS': '#ff7f0e', 
                        'TWEET_POSTS': '#2ca02c'
                    }
                )
                fig_trends.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Count",
                    legend_title="Metrics"
                )
                st.plotly_chart(fig_trends, use_container_width=True)
            else:
                st.info("📊 Need more data points to show trends. Come back after using the app more!")
            
            # AI Provider Performance
            st.subheader("🤖 AI Provider Performance")
            
            if not ai_performance.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Provider usage pie chart
                    fig_pie = px.pie(
                        ai_performance,
                        values='TOTAL_REQUESTS',
                        names='AI_PROVIDER',
                        title="AI Provider Usage Distribution"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col2:
                    # Performance metrics bar chart
                    fig_bar = px.bar(
                        ai_performance,
                        x='AI_PROVIDER',
                        y='AVG_PROCESSING_TIME_MS',
                        title="Average Processing Time by Provider",
                        labels={'AVG_PROCESSING_TIME_MS': 'Avg Time (ms)'}
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                # Detailed performance table
                st.subheader("📊 Detailed AI Provider Metrics")
                
                # Format the dataframe for display
                display_df = ai_performance.copy()
                display_df['SUCCESS_RATE_PERCENT'] = display_df['SUCCESS_RATE_PERCENT'].round(1)
                display_df['AVG_PROCESSING_TIME_MS'] = display_df['AVG_PROCESSING_TIME_MS'].round(0)
                
                st.dataframe(
                    display_df,
                    column_config={
                        "AI_PROVIDER": "Provider",
                        "TOTAL_REQUESTS": st.column_config.NumberColumn("Total Requests", format="%d"),
                        "AVG_PROCESSING_TIME_MS": st.column_config.NumberColumn("Avg Time (ms)", format="%.0f"),
                        "SUCCESSFUL_REQUESTS": st.column_config.NumberColumn("Successful", format="%d"),
                        "FAILED_REQUESTS": st.column_config.NumberColumn("Failed", format="%d"),
                        "SUCCESS_RATE_PERCENT": st.column_config.NumberColumn("Success Rate", format="%.1f%%")
                    },
                    use_container_width=True
                )
            else:
                st.info("🤖 No AI provider data available yet. Generate some tweets to see performance metrics!")
            
            # Recent Content
            st.subheader("📝 Recent Generated Content")
            
            if not recent_content.empty:
                # Show recent content in an expandable format
                for idx, row in recent_content.head(10).iterrows():
                    with st.expander(f"🤖 {row['AI_PROVIDER'].title()} - {row['GENERATION_TIMESTAMP'].strftime('%Y-%m-%d %H:%M')}"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write("**Generated Text:**")
                            st.write(f"_{row['GENERATED_TEXT']}_")
                            st.write(f"**Characters:** {row['CHARACTER_COUNT']}")
                            
                        with col2:
                            st.write(f"**File:** {row['ORIGINAL_FILENAME']}")
                            st.write(f"**Status:** {row['POST_STATUS']}")
                            st.write(f"**Provider:** {row['AI_PROVIDER'].title()}")
            else:
                st.info("📝 No content generated yet. Upload images and generate tweets to see them here!")
            
            # Success/Failure Analysis
            st.subheader("📊 Success/Failure Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Success rate over time
                if len(usage_stats) > 1:
                    usage_stats['success_rate'] = (usage_stats['SUCCESSFUL_EVENTS'] / usage_stats['TOTAL_EVENTS'] * 100).fillna(0)
                    
                    fig_success = px.line(
                        usage_stats,
                        x='USAGE_DATE',
                        y='success_rate',
                        title="Success Rate Over Time",
                        labels={'success_rate': 'Success Rate (%)', 'USAGE_DATE': 'Date'}
                    )
                    fig_success.update_traces(line_color='#2ca02c')
                    fig_success.update_layout(yaxis_range=[0, 100])
                    st.plotly_chart(fig_success, use_container_width=True)
            
            with col2:
                # Success vs Failure pie chart
                total_success = usage_stats['SUCCESSFUL_EVENTS'].sum()
                total_failure = usage_stats['FAILED_EVENTS'].sum()
                
                if total_success + total_failure > 0:
                    success_data = pd.DataFrame({
                        'Status': ['Success', 'Failure'],
                        'Count': [total_success, total_failure]
                    })
                    
                    fig_success_pie = px.pie(
                        success_data,
                        values='Count',
                        names='Status',
                        title="Overall Success vs Failure",
                        color_discrete_map={'Success': '#2ca02c', 'Failure': '#d62728'}
                    )
                    st.plotly_chart(fig_success_pie, use_container_width=True)
        
        else:
            st.info("📊 No usage data available yet. Start using the app to generate analytics!")
            
            # Show sample data structure
            st.subheader("📋 What You'll See Here")
            st.write("""
            Once you start using TweeterBot, this dashboard will show:
            
            - **📈 Usage Trends**: Daily counts of images uploaded, AI generations, and tweets posted
            - **🤖 AI Provider Performance**: Which AI providers you use most and their response times
            - **📝 Recent Content**: Your latest generated tweets and their status
            - **📊 Success Metrics**: Success rates and failure analysis
            - **💰 Cost Tracking**: Estimated API costs (coming soon)
            """)
    
    except Exception as e:
        st.error(f"❌ Error loading analytics data: {str(e)}")
        st.info("💡 Make sure your Snowflake connection is properly configured.")

def show_data_export():
    """Show data export options"""
    st.subheader("📤 Data Export")
    
    if not st.session_state.get('snowflake_connected', False):
        st.error("❌ Snowflake not connected. Data export requires database connection.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Usage Statistics"):
            try:
                usage_stats = snowflake_manager.get_daily_usage_stats(90)
                if not usage_stats.empty:
                    csv = usage_stats.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"tweeterbot_usage_stats_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No data available to export")
            except Exception as e:
                st.error(f"Export failed: {str(e)}")
    
    with col2:
        if st.button("📝 Export Generated Content"):
            try:
                content_data = snowflake_manager.get_recent_content(1000)
                if not content_data.empty:
                    csv = content_data.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"tweeterbot_content_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No content available to export")
            except Exception as e:
                st.error(f"Export failed: {str(e)}")

if __name__ == "__main__":
    show_analytics_dashboard()
