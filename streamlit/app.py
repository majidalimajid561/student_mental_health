"""
Student Mental Health Score Prediction — Streamlit App
Author: Your Name
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
from pathlib import Path

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Student Mental Health Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. PATHS & MODEL LOADING
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "random_forest.pkl"

@st.cache_resource
def load_model():
    """Load the trained pipeline (preprocessing + model)."""
    if not MODEL_PATH.exists():
        st.error(f"❌ Model file not found at: {MODEL_PATH}")
        st.stop()
    return joblib.load(MODEL_PATH)



pipeline = load_model()

# ============================================================
# 3. CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 35px 30px;
        border-radius: 18px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(102,126,234,0.3);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.3rem;
        font-weight: 700;
    }
    .main-header p {
        color: #e0e7ff;
        margin-top: 10px;
        font-size: 1.05rem;
    }

    /* Section headers */
    .section-title {
        color: #4c51bf;
        font-weight: 600;
        font-size: 1.15rem;
        margin: 15px 0 10px 0;
        padding-bottom: 6px;
        border-bottom: 2px solid #c7d2fe;
    }

    /* Result cards */
    .result-card {
        padding: 30px;
        border-radius: 18px;
        text-align: center;
        color: white;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        animation: fadeIn 0.6s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .result-excellent { background: linear-gradient(135deg, #10b981, #34d399); }
    .result-good      { background: linear-gradient(135deg, #3b82f6, #60a5fa); }
    .result-moderate  { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
    .result-poor      { background: linear-gradient(135deg, #ef4444, #f87171); }

    .result-card h2 { color: white; font-size: 1.9rem; margin: 0 0 8px 0; }
    .result-card .score-value {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 15px 0;
        letter-spacing: 2px;
    }
    .result-card p { color: white; font-size: 1.05rem; margin: 5px 0; }
    .result-card .poetic {
        font-style: italic;
        font-size: 1.05rem;
        margin-top: 15px;
        opacity: 0.95;
    }

    /* Metric cards */
    .metric-card {
        background: #f8fafc;
        border-left: 5px solid #667eea;
        padding: 15px 18px;
        border-radius: 10px;
        margin: 8px 0;
    }
    .metric-card h4 {
        margin: 0;
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .metric-card .value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 4px;
    }

    /* Submit button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 14px 30px;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102,126,234,0.35);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102,126,234,0.5);
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 4. HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🧠 Student Mental Health Predictor</h1>
    <p>Understand how your daily habits shape your mental well-being</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# 6. INPUT FORM
# ============================================================
st.markdown("## 📋 Enter Your Details")

with st.form("prediction_form"):
    # ---------- Section 1: Personal Info ----------
    st.markdown('<div class="section-title">👤 Personal Information</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input(
            "Age", min_value=15, max_value=30, value=21, step=1,
            help="Your current age in years"
        )
    with col2:
        gender = st.selectbox(
            "Gender",
            options=["Male", "Female", "Other"]
        )
    with col3:
        country = st.text_input(
            "Country", value="Pakistan",
            help="Your country of residence"
        )

    col4, col5 = st.columns(2)
    with col4:
        academic_level = st.selectbox(
            "Academic Level",
            options=['Undergraduate', 'Graduate', 'High School']
        )
    with col5:
        stress_level = st.selectbox(
            "Stress Level",
            options=['Very High', 'High', 'Medium', 'Low']
        )

    # ---------- Section 2: Social Media Usage ----------
    st.markdown('<div class="section-title">📱 Social Media Habits</div>', unsafe_allow_html=True)
    col6, col7 = st.columns(2)

    with col6:
        most_used_platform = st.selectbox(
            "Most Used Platform",
            options=["Instagram", "Facebook", "TikTok", "Twitter",
                     "YouTube", "Snapchat", "LinkedIn", "Other"]
        )
    with col7:
        purpose_of_use = st.selectbox(
            "Purpose of Use",
            options=["Education", "Entertainment", "Socializing",
                     "Work", "News", "Other"]
        )

    col8, col9 = st.columns(2)
    with col8:
        avg_daily_usage = st.slider(
            "Average Daily Usage (hours)",
            min_value=0.0, max_value=24.0, value=4.0, step=0.5,
            help="Hours spent on social media per day"
        )
    with col9:
        daily_unlocks = st.slider(
            "Daily Phone Unlocks",
            min_value=0, max_value=500, value=100, step=5,
            help="How many times you unlock your phone per day"
        )

    # ---------- Section 3: Lifestyle ----------
    st.markdown('<div class="section-title">🏃 Lifestyle Habits</div>', unsafe_allow_html=True)
    col10, col11, col12 = st.columns(3)

    with col10:
        study_hours = st.slider(
            "Study Hours (per day)",
            min_value=0.0, max_value=16.0, value=4.0, step=0.5
        )
    with col11:
        physical_activity = st.slider(
            "Physical Activity (hours)",
            min_value=0.0, max_value=8.0, value=1.0, step=0.5
        )
    with col12:
        sleep_hours = st.slider(
            "Sleep (hours per night)",
            min_value=0.0, max_value=12.0, value=7.0, step=0.5
        )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔮 Predict My Mental Health Score", use_container_width=True)


# ============================================================
# 7. PREDICTION LOGIC
# ============================================================
def get_result_color(score, max_score=10):
    """Return CSS class based on predicted score."""
    if score >= 8:
        return "result-excellent", "🌟 Excellent", "Your mental well-being is thriving!"
    elif score >= 6.5:
        return "result-good", "✅ Good", "You're doing well — keep nurturing your habits."
    elif score >= 5:
        return "result-moderate", "⚠️ Moderate", "Some areas need attention. Small changes matter."
    else:
        return "result-poor", "🆘 Needs Care", "Consider reaching out for support — you matter."


def get_poetic_line(score):
    """Return a meaningful line based on the score."""
    if score >= 8:
        return "“Your mind is a garden in full bloom — keep watering it with rest and joy.”"
    elif score >= 6.5:
        return "“Steady roots, gentle growth. You are exactly where you need to be.”"
    elif score >= 5:
        return "“Even the tallest trees sway in storms. Be kind to yourself today.”"
    else:
        return "“Storms pass. The sun always returns — and so will your light.”"


if submitted:
    # Build input DataFrame — column names MUST match training data
    input_df = pd.DataFrame({
        "Age": [age],
        "Gender": [gender],
        "Country": [country],
        "Academic_Level": [academic_level],
        "Most_Used_Platform": [most_used_platform],
        "Purpose_Of_Use": [purpose_of_use],
        "Avg_Daily_Usage_Hours": [avg_daily_usage],
        "Daily_Unlocks": [daily_unlocks],
        "Study_Hours": [study_hours],
        "Physical_Activity_Hours": [physical_activity],
        "Sleep_Hours_Per_Night": [sleep_hours],
        "Stress_Level": [stress_level]
    })

    with st.spinner("🔍 Analyzing your habits..."):
        try:
            prediction = float(pipeline.predict(input_df)[0])
            # Clamp between 0 and 10 (adjust if your target range differs)
            prediction = max(0.0, min(10.0, prediction))
        except Exception as e:
            st.error(f"Prediction error: {e}")
            st.stop()

    st.markdown("---")
    st.markdown("## 🎯 Your Predicted Mental Health Score")

    css_class, label, message = get_result_color(prediction)
    poetic = get_poetic_line(prediction)

    st.markdown(f"""
    <div class="result-card {css_class}">
        <h2>{label}</h2>
        <div class="score-value">{prediction:.2f} / 10</div>
        <p>{message}</p>
        <p class="poetic">{poetic}</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Detailed Breakdown ----------
    st.markdown("### 📊 Score Breakdown")

    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Predicted Score</h4>
            <div class="value">{prediction:.2f}</div>
        </div>
        """, unsafe_allow_html=True)


    # ---------- Visual Gauge ----------
    st.markdown("### 📈 Score Meter")
    st.progress(prediction / 10.0)

    # ---------- Input Summary ----------
    with st.expander("🔍 View Your Submitted Details"):
        st.dataframe(
            input_df.T.rename(columns={0: "Your Value"}),
            use_container_width=True
        )

    # ---------- Disclaimer ----------
    st.markdown("---")
    st.caption(
        "⚠️ **Disclaimer:** This prediction is based on a machine learning model "
        "trained on survey data. It is not a substitute for professional mental "
        "health advice. If you're struggling, please reach out to a trusted person "
        "or a professional."
    )


# ============================================================
# 8. FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#94a3b8; font-size:0.9rem;'>"
    "Built with ❤️ using Streamlit & Random Forest Regressor"
    "</p>",
    unsafe_allow_html=True
)
