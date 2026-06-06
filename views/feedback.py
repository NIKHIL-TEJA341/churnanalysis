import streamlit as st

def get_sentiment_category(compound_score):
    if compound_score >= 0.5:
        return "Excellent", "#118ab2"
    elif compound_score >= 0.1:
        return "Good", "#06d6a0"
    elif compound_score > -0.1:
        return "OK", "#ffd166"
    elif compound_score > -0.5:
        return "Bad", "#fca120"
    else:
        return "Worst", "#ff4b4b"

def render(analyzer):
    st.markdown("<h2>Feedback Analysis Center</h2>", unsafe_allow_html=True)
    st.caption("Analyze real-time sentiment from customer feedback.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Raw Customer Input")
        feedback_text = st.text_area("Review", height=200, placeholder="Enter customer feedback here to instantly analyze sentiment...", label_visibility="collapsed")
        
        st.markdown("#### Real-time Sentiment")
        
        if feedback_text:
            scores = analyzer.polarity_scores(feedback_text)
            compound = scores['compound']
            category, color = get_sentiment_category(compound)
            
            st.markdown(f"""
                <div style='width: 100%; height: 8px; border-radius: 4px; background: linear-gradient(90deg, #ff4b4b 0%, #fca120 25%, #ffd166 50%, #06d6a0 75%, #118ab2 100%); margin-top: 15px;'></div>
                <h1 style='color:{color}; margin-top:20px; font-size:3rem;'>{category}</h1>
                <p style='color:#fb5607; font-weight:600; font-size: 1.2rem;'>CONFIDENCE: {abs(compound)*100:.1f}%</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='width: 100%; height: 8px; border-radius: 4px; background: rgba(0,0,0,0.05); margin-top: 15px;'></div>
                <h1 style='color:gray; margin-top:20px; font-size:3rem;'>Waiting...</h1>
                <p style='color:gray; font-size: 1.2rem;'>CONFIDENCE: 0%</p>
            """, unsafe_allow_html=True)
            
    with col2:
        if feedback_text:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Individual styling ratios because the images have different aspect ratios
            if category == "Excellent":
                ratio = [1, 6, 1]
            elif category == "Good":
                ratio = [1, 5, 1]
            elif category == "OK":
                ratio = [1, 4, 1]
            elif category == "Bad":
                ratio = [1, 3, 1]
            else: # Worst
                ratio = [1, 2, 1]
                
            img_col1, img_col2, img_col3 = st.columns(ratio)
            with img_col2:
                sentiment_images = {
                    "Excellent": "great1.png",
                    "Good": "good1.png",
                    "OK": "ok1.png",
                    "Bad": "bad1.png",
                    "Worst": "worst1.png"
                }
                img_path = sentiment_images.get(category, "")
                st.image(img_path, use_container_width=True)
        else:
            st.image("feedbackgimg.png", use_container_width=True)
