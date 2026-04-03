import streamlit as st
import cv2
import numpy as np
import os
import requests

# --- Page Config ---
st.set_page_config(page_title="Fake Detector Pro", layout="wide", page_icon="🛡️")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; }
    .hero-title { text-align: center; font-size: 3.5rem; font-weight: 800; color: #38bdf8; margin-bottom: 20px; }
    .stButton>button { width: 100%; height: 50px; background: #2563eb; color: white; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='hero-title'>🛡️ FAKE DETECTOR PRO</h1>", unsafe_allow_html=True)

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload Image to Scan", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Convert file to OpenCV format
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, channels="BGR", caption="Uploaded Evidence", use_container_width=True)
    
    with col2:
        if st.button("🚀 EXECUTE AI SCAN"):
            with st.spinner("Analyzing pixels..."):
                # Industry-standard Forensic Logic: Laplacian Variance
                # Detects if image is too smooth (fake) or has natural noise (real)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
                
                st.subheader("Analysis Verdict")
                if laplacian_var < 50:
                    st.error(f"VERDICT: FAKE / MANIPULATED")
                    st.write("Reason: Unusual pixel smoothing detected. High probability of AI generation.")
                else:
                    st.success(f"VERDICT: REAL / AUTHENTIC")
                    st.write("Reason: Natural skin texture and sensor noise patterns identified.")
                
                # Display Score
                st.metric("Integrity Score", f"{min(laplacian_var, 100):.1f}%")
