import streamlit as st
import pandas as pd
from utils import CAT_MAPPINGS

def render(df, model, feature_names):
    st.markdown("<h2>Prediction Wizard</h2>", unsafe_allow_html=True)
    
    if 'pred_step' not in st.session_state:
        st.session_state.pred_step = 1
        st.session_state.pred_target_id = None
        st.session_state.pred_result = None

    if st.session_state.pred_step == 1:
        st.caption("Step 1: Locate Customer Record")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("<br><br>", unsafe_allow_html=True)
            search_id = st.text_input("Enter Customer ID to Begin", placeholder="e.g., 50001", key="pred_search")
            
            if search_id:
                try:
                    target_id = int(search_id)
                    customer_data = df[df['CustomerID'] == target_id]
                    
                    if customer_data.empty:
                        st.error("❌ Customer Record Not Found in Dataset.")
                    else:
                        c = customer_data.iloc[0]
                        st.success("✅ Customer Verified!")
                        
                        st.markdown("#### Key Identifiers")
                        metrics_col1, metrics_col2 = st.columns(2)
                        
                        gender_str = CAT_MAPPINGS['Gender'].get(int(c['Gender']), 'Unknown')
                        order_cat_str = CAT_MAPPINGS['PreferedOrderCat'].get(int(c['PreferedOrderCat']), 'Unknown')
                        
                        with metrics_col1:
                            st.markdown(f"<div class='premium-card' style='padding:15px; margin-bottom:10px;'><p style='margin:0; font-size:0.8rem; color:gray;'>Gender</p><h4 style='margin:0; color:#0ea5e9;'>{gender_str}</h4></div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='premium-card' style='padding:15px; margin-bottom:10px;'><p style='margin:0; font-size:0.8rem; color:gray;'>Product Category</p><h4 style='margin:0; color:#0ea5e9;'>{order_cat_str}</h4></div>", unsafe_allow_html=True)
                        with metrics_col2:
                            st.markdown(f"<div class='premium-card' style='padding:15px; margin-bottom:10px;'><p style='margin:0; font-size:0.8rem; color:gray;'>Tenure</p><h4 style='margin:0; color:#0ea5e9;'>{c['Tenure']} Months</h4></div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='premium-card' style='padding:15px; margin-bottom:10px;'><p style='margin:0; font-size:0.8rem; color:gray;'>Satisfaction</p><h4 style='margin:0; color:#0ea5e9;'>{c['SatisfactionScore']}/5</h4></div>", unsafe_allow_html=True)
                            
                        if st.button("Proceed to Prediction ➡️", type="primary", use_container_width=True):
                            st.session_state.pred_target_id = target_id
                            st.session_state.pred_step = 2
                            st.rerun()
                            
                except ValueError:
                    st.warning("Please enter a valid numeric Customer ID.")
                    
        with col2:
            st.image("prediction.png", use_container_width=True)

    elif st.session_state.pred_step == 2:
        st.caption(f"Step 2: Verify & Edit Profile (ID: {st.session_state.pred_target_id})")
        if st.button("⬅️ Back to Search"):
            st.session_state.pred_step = 1
            st.rerun()
            
        c = df[df['CustomerID'] == st.session_state.pred_target_id].iloc[0]
        
        with st.form("simulation_form"):
            st.markdown("### Profile Attributes")
            st.caption("Please verify or modify the customer details below before running the model.")
            
            cols = st.columns(3)
            input_data = {}
            
            for i, feature in enumerate(feature_names):
                val = float(c[feature]) if pd.notnull(c[feature]) else 0.0
                with cols[i % 3]:
                    if feature in CAT_MAPPINGS:
                        options_dict = CAT_MAPPINGS[feature]
                        current_int = int(val)
                        current_str = options_dict.get(current_int, list(options_dict.values())[0])
                        options_list = list(options_dict.values())
                        
                        selected_str = st.selectbox(f"{feature}", options=options_list, index=options_list.index(current_str))
                        reverse_dict = {v: k for k, v in options_dict.items()}
                        input_data[feature] = reverse_dict[selected_str]
                    else:
                        input_data[feature] = st.number_input(f"{feature}", value=val, step=1.0)
                        
            submit = st.form_submit_button("Run Prediction 🚀", type="primary")
            
            if submit:
                input_df = pd.DataFrame([input_data])
                prediction = model.predict(input_df)[0]
                prob = model.predict_proba(input_df)[0]
                confidence = prob[1] if prediction == 1 else prob[0]
                
                st.session_state.pred_result = {
                    'prediction': prediction,
                    'confidence': confidence
                }
                st.session_state.pred_step = 3
                st.rerun()

    elif st.session_state.pred_step == 3:
        st.caption("Step 3: Inference Results")
        
        res = st.session_state.pred_result
        prediction = res['prediction']
        confidence = res['confidence']
        
        result_text = "DISCONTINUING PRODUCT" if prediction == 1 else "CONTINUING PRODUCT"
        result_color = "#ff4b4b" if prediction == 1 else "#0ea5e9"
        
        st.markdown(f"""
        <div class='premium-card' style='margin-top:20px; display:flex; justify-content:space-between; align-items:center; background: rgba(15,23,42,0.6); border-color: {result_color}; padding: 40px;'>
            <div>
                <p style='color:{result_color}; font-weight:bold; font-size:1.2rem; margin:0; letter-spacing: 2px;'>LIVE MODEL INFERENCE RESULT</p>
                <h1 style='color:{result_color}; font-size:4rem; margin:10px 0;'>{result_text}</h1>
            </div>
            <div style='width: 200px; height: 200px; border-radius: 50%; background: conic-gradient({result_color} {confidence*100}%, rgba(255,255,255,0.05) 0); display: flex; align-items: center; justify-content: center; position: relative;'>
                <div style='width: 170px; height: 170px; border-radius: 50%; background: #090e17; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: inset 0 0 15px rgba(0,0,0,0.5);'>
                    <h2 style='margin:0; font-size:3rem; color:#ffffff;'>{confidence*100:.0f}%</h2>
                    <p style='margin:0; font-size:1rem; color:#cbd5e1; font-weight:600;'>CONFIDENCE</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ Go Back & Edit Inputs", type="primary"):
            st.session_state.pred_step = 2
            st.rerun()
        
        if st.button("🔍 Search New Customer"):
            st.session_state.pred_step = 1
            st.rerun()
