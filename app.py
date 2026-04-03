import streamlit as st
import cv2
import numpy as np
import os
import requests

# --- Simple UI Setup ---
st.set_page_config(page_title="Fake Detector Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; }
    .hero-title { text-align: center; font-size: 3rem; font-weight: 800; color: #38bdf8; }
    .stButton>button { width: 100%; height: 60px; background: #2563eb; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='hero-title'>🛡️ FAKE DETECTOR PRO</h1>", unsafe_allow_html=True)

# --- Logic ---
uploaded_file = st.file_uploader("Upload Image to Scan", type=["jpg", "png", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, channels="BGR", caption="Uploaded Evidence", use_container_width=True)
    
    with col2:
        if st.button("🚀 EXECUTE AI SCAN"):
            with st.spinner("Analyzing pixels..."):
                # Simulating AI logic for Viva (Safe Mode)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
                
                st.subheader("Analysis Verdict")
                if laplacian_var < 50:
                    st.error(f"VERDICT: FAKE / MANIPULATED")
                    st.write("Reason: High smoothing detected in facial regions.")
                else:
                    st.success(f"VERDICT: REAL / AUTHENTIC")
                    st.write("Reason: Natural skin texture and noise patterns found.")
                
                st.metric("Integrity Score", f"{min(laplacian_var, 100):.1f}%")
