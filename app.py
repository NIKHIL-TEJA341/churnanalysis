import streamlit as st
from utils import inject_global_css, load_models_and_data, load_data_from_db


st.set_page_config(page_title="E-Commerce Churn Predictor", layout="wide")


inject_global_css()


st.markdown("<h1 style='text-align: center; color: #ffffff; margin-bottom: 20px;'>E-Commerce<span style='color:#0ea5e9;'> Churn Predictor</span></h1>", unsafe_allow_html=True)


if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Insights'


col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📊 Global Insights", use_container_width=True):
        st.session_state.current_page = 'Insights'
with col2:
    if st.button("🔍 Intelligence", use_container_width=True):
        st.session_state.current_page = 'Intelligence'
with col3:
    if st.button("⚡ Predictions", use_container_width=True):
        st.session_state.current_page = 'Predictions'
with col4:
    if st.button("💬 Feedback", use_container_width=True):
        st.session_state.current_page = 'Feedback'

st.markdown("<hr style='border:1px solid rgba(0,0,0,0.1);'>", unsafe_allow_html=True)


model, feature_names, analyzer = load_models_and_data()
df = load_data_from_db()

if df is None:
    st.error("Database not found! Please run `python init_db.py`.")
    st.stop()


if st.session_state.current_page == 'Insights':
    from views.insights import render
    render(df)
elif st.session_state.current_page == 'Intelligence':
    from views.profile import render
    render(df)
elif st.session_state.current_page == 'Predictions':
    from views.predictions import render
    render(df, model, feature_names)
elif st.session_state.current_page == 'Feedback':
    from views.feedback import render
    render(analyzer)
