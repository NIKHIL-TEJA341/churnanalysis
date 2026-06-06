import streamlit as st
import plotly.express as px

def render(df):
    st.markdown("<h2>Advanced Analytics</h2>", unsafe_allow_html=True)
    st.caption("Cyberpunk Pink/Orange theme for macro-level distribution analysis.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Churn Distribution")
        churn_counts = df['Churn'].value_counts().reset_index()
        churn_counts['Churn'] = churn_counts['Churn'].map({0: 'Continuing', 1: 'Discontinuing'})
        fig = px.pie(churn_counts, values='count', names='Churn', hole=0.75, 
                     color='Churn', color_discrete_map={'Continuing': '#00f2fe', 'Discontinuing': '#ff007f'},
                     template='plotly_white')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0), height=300)
        st.plotly_chart(fig)
        
    with col2:
        st.markdown("#### Cashback vs Tenure Correlation")
        fig2 = px.scatter(df, x='Tenure', y='CashbackAmount', color='Churn',
                      template='plotly_white', color_continuous_scale=['#00f2fe', '#ff007f'])
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0), height=300)
        st.plotly_chart(fig2)
