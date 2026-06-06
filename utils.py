import streamlit as st
import sqlite3
import pandas as pd
import joblib
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def inject_global_css():
    st.markdown("""
        <style>
        /* Hide Streamlit Default UI Elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        [data-testid="stSidebar"] {display: none;} /* Completely hide sidebar */
        
        /* Base Background and Text */
        .stApp {
            background-color: #090e17; /* Dark Blue */
            color: #ffffff; /* White text */
            font-family: 'Inter', 'Outfit', sans-serif;
            background-image: radial-gradient(#1e293b 1px, transparent 1px);
            background-size: 20px 20px;
        }
        
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 1400px;
        }
        
        /* Metric Cards */
        [data-testid="stMetricValue"] {
            font-size: 2.5rem !important;
            font-weight: 700;
            background: linear-gradient(90deg, #0ea5e9, #00f2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Glassmorphism Premium Cards */
        .premium-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(14, 165, 233, 0.3);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(12px);
            margin-bottom: 24px;
            box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
        }
        .premium-card:hover {
            transform: translateY(-4px);
            border-color: rgba(0, 242, 254, 0.8);
            box-shadow: 0 12px 24px 0 rgba(0, 242, 254, 0.3);
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        
        /* Neon Accents */
        .neon-text {
            color: #0ea5e9;
            text-shadow: 0 0 10px rgba(14, 165, 233, 0.5);
        }
        
        /* Inputs styling override */
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: rgba(15, 23, 42, 0.8) !important;
            color: #ffffff !important;
            border: 1px solid #1e293b !important;
            border-radius: 8px !important;
        }
        
        /* Buttons */
        .stButton>button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s;
            border: 1px solid rgba(14, 165, 233, 0.5) !important;
            background: rgba(15, 23, 42, 0.8) !important;
            color: #ffffff !important;
        }
        .stButton>button:hover {
            border-color: #00f2fe !important;
            color: #ffffff !important;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.4) !important;
            background: rgba(14, 165, 233, 0.2) !important;
        }
        
        /* Form background */
        [data-testid="stForm"] {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(14, 165, 233, 0.3);
            border-radius: 16px;
        }
        
        /* Text overrides for generic markdown */
        p, span, div {
            color: #e2e8f0; /* Soft white for readability */
        }
        </style>
    """, unsafe_allow_html=True)

def get_db_connection():
    return sqlite3.connect('database.db', check_same_thread=False)

@st.cache_resource
def load_models_and_data():
    try:
        model = joblib.load('best_model.pkl')
        feature_names = joblib.load('feature_names.pkl')
        analyzer = SentimentIntensityAnalyzer()
        return model, feature_names, analyzer
    except Exception as e:
        st.error(f"Error loading models. Error details: {e}")
        return None, None, None

@st.cache_data
def load_data_from_db():
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM Customers", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return None

CAT_MAPPINGS = {
    'Gender': {0: 'Female', 1: 'Male'},
    'MaritalStatus': {0: 'Divorced', 1: 'Married', 2: 'Single'},
    'Complain': {0: 'No', 1: 'Yes'},
    'PreferredLoginDevice': {0: 'Computer', 1: 'Mobile Phone', 2: 'Phone'},
    'PreferedOrderCat': {0: 'Fashion', 1: 'Grocery', 2: 'Laptop & Accessory', 3: 'Mobile', 4: 'Mobile Phone', 5: 'Others'},
    'PreferredPaymentMode': {0: 'CC', 1: 'COD', 2: 'Cash on Delivery', 3: 'Credit Card', 4: 'Debit Card', 5: 'E wallet', 6: 'UPI'}
}
