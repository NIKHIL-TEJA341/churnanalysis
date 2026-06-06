import streamlit as st
from utils import CAT_MAPPINGS

def render(df):
    st.markdown("<h2>Customer Profile Search</h2>", unsafe_allow_html=True)
    st.caption("Search for a customer by their ID to securely view their demographic and purchasing history.")
    
    search_id = st.text_input("Customer ID", placeholder="Enter ID to view profile (e.g. 50001)")
    
    if search_id:
        try:
            cid = int(search_id)
            customer = df[df['CustomerID'] == cid]
            if not customer.empty:
                c = customer.iloc[0]
                

                st.markdown(f"""
                <div class='premium-card' style='border-color: #7b2cbf; display:flex; justify-content:space-between; align-items:center;'>
                    <div style='display:flex; gap: 20px; align-items:center;'>
                        <div style='width:60px; height:60px; border-radius:30px; background:linear-gradient(135deg, #7b2cbf, #c77dff); display:flex; justify-content:center; align-items:center; font-size:24px;'>
                            👤
                        </div>
                        <div>
                            <h3 style='margin:0;'>{c['CustomerName']}</h3>
                            <p style='color:#c77dff; margin:0; font-size:0.8rem; font-weight:600;'>ID: {cid} • Active Profile</p>
                        </div>
                    </div>
                    <div style='text-align:right;'>
                        <p style='margin:0; font-size:0.8rem; color:gray;'>Days Since Last Order</p>
                        <h2 style='margin:0; color:#c77dff;'>{c['DaySinceLastOrder']} days</h2>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col_chart = st.columns([1, 1, 1, 2])
                with col1:
                    order_cat_str = CAT_MAPPINGS['PreferedOrderCat'].get(int(c['PreferedOrderCat']), 'Unknown')
                    st.markdown(f"<div class='premium-card' style='border-color: #7b2cbf;'><h4>PRODUCT</h4><h3 style='color:#c77dff;'>{order_cat_str}</h3></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='premium-card' style='border-color: #7b2cbf;'><h4>CASHBACK</h4><h3 style='color:#c77dff;'>${c['CashbackAmount']}</h3></div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='premium-card' style='border-color: #7b2cbf;'><h4>ORDERS</h4><h3 style='color:#c77dff;'>{c['OrderCount']}</h3></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='premium-card' style='border-color: #7b2cbf;'><h4>RATING</h4><h3 style='color:#c77dff;'>{c['SatisfactionScore']}/5</h3></div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div class='premium-card' style='border-color: #7b2cbf;'><h4>TENURE</h4><h3 style='color:#c77dff;'>{c['Tenure']} mo</h3></div>", unsafe_allow_html=True)
                    complain_str = CAT_MAPPINGS['Complain'].get(int(c['Complain']), 'Unknown')
                    st.markdown(f"<div class='premium-card' style='border-color: #7b2cbf;'><h4>ISSUES</h4><h3 style='color:#c77dff;'>{complain_str}</h3></div>", unsafe_allow_html=True)
                
                with col_chart:
                    st.markdown("<div style='display:flex; justify-content:center; align-items:center; height:100%;'>", unsafe_allow_html=True)
                    st.image("found.png", use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("Customer not found in the dataset.")
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    st.image("notfound.png", use_container_width=True)
        except ValueError:
            st.warning("Please enter a valid numeric Customer ID.")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            st.image("searching.png", use_container_width=True)
