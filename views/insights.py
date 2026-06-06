import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def render(df):
    st.markdown("<h2>Global Insights Hub</h2>", unsafe_allow_html=True)
    st.caption("A comprehensive view of the entire dataset's health, demographics, and churn metrics.")
    
    st.markdown("""
    <div class='premium-card' style='padding: 15px; margin-bottom: 20px;'>
        <h4 style='margin-top: 0; color: #0ea5e9;'>Dataset: Ecommerce Customer Churn Analysis and Prediction</h4>
        <p style='color: #e2e8f0; margin-bottom: 0;'>
        This dataset tracks e-commerce customer behavior to predict customer churn and make suggestions. 
        It contains records for thousands of customers with <b>{} features</b> per customer, such as <i>Tenure, Preferred Login Device, City Tier, Preferred Payment Mode, Gender, Satisfaction Score, Order Count, and Cashback Amount</i>.
        </p>
    </div>
    """.format(len(df.columns)), unsafe_allow_html=True)
    
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
    fig1 = px.line(trend_df, x='Tenure', y='SatisfactionScore', template="plotly_white")
    fig1.update_traces(line_color='#0ea5e9', line_width=3, fill='tozeroy', fillcolor='rgba(14, 165, 233, 0.1)')
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Tenure (Months)", yaxis_title="Average Satisfaction (1-5)")
    st.plotly_chart(fig1)

    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Churn Distribution")
        churn_counts = df['Churn'].value_counts().reset_index()
        churn_counts['Churn'] = churn_counts['Churn'].map({0: 'Continuing', 1: 'Discontinuing'})
        fig2 = px.pie(churn_counts, values='count', names='Churn', hole=0.75, 
                     color='Churn', color_discrete_map={'Continuing': '#0ea5e9', 'Discontinuing': '#ff007f'},
                     template='plotly_white')
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0), height=300)
        st.plotly_chart(fig2)
        
    with col_b:
        st.markdown("#### Churn by Gender")
        gender_churn = df.groupby(['Gender', 'Churn']).size().reset_index(name='Count')
        gender_churn['Gender'] = gender_churn['Gender'].map({0: 'Female', 1: 'Male'})
        gender_churn['Churn'] = gender_churn['Churn'].map({0: 'Continuing', 1: 'Discontinuing'})
        
        fig3 = px.bar(gender_churn, x='Gender', y='Count', color='Churn', barmode='group',
                      color_discrete_map={'Continuing': '#0ea5e9', 'Discontinuing': '#ff007f'},
                      template='plotly_white')
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0), height=300)
        st.plotly_chart(fig3)
