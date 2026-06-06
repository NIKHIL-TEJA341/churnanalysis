import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def render(df):
    st.markdown("<h2>Dashboard Overview</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Customers", f"{len(df):,}")
    with col2:
        churn_count = len(df[df['Churn'] == 1])
        st.metric("Total Churned", f"{churn_count:,}")
    with col3:
        retention_rate = round((len(df[df['Churn']==0]) / len(df)) * 100, 1)
        st.metric("Retention Rate", f"{retention_rate}%")
    with col4:
        avg_satisfaction = round(df['SatisfactionScore'].mean(), 1)
        st.metric("Avg. Satisfaction", f"{avg_satisfaction}/5")
        
    st.markdown("### Average Satisfaction Score by Tenure")
    trend_df = df.groupby('Tenure')['SatisfactionScore'].mean().reset_index()
    fig = px.line(trend_df, x='Tenure', y='SatisfactionScore', template="plotly_white")
    # Vibrant neon blue line
    fig.update_traces(line_color='#00f2fe', line_width=3, fill='tozeroy', fillcolor='rgba(0, 242, 254, 0.1)')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Tenure (Months)", yaxis_title="Average Satisfaction (1-5)")
    st.plotly_chart(fig)
