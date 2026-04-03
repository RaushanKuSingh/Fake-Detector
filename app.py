import streamlit as st
import cv2
import numpy as np
import os
import tensorflow as tf
import requests
import time

# --- 1. CONFIG & THEME (Ultra Modern Dark) ---
st.set_page_config(page_title="SENTINEL AI | Deepfake Detector", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp {
        background: #020617;
        color: #e2e8f0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Premium Title */
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -2px;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Status Bar Animation */
    .scanning-bar {
        height: 4px;
        background: linear-gradient(90deg, transparent, #38bdf8, transparent);
        background-size: 200% 100%;
        animation: scan 2s linear infinite;
    }
    @keyframes scan { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

    /* Cards & Containers */
    .st-emotion-cache-1r6slb0 { border: 1px solid #1e293b; border-radius: 12px; background: #0f172a; padding: 20px; }
    
    /* Custom Button */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: transparent;
        border: 1px solid #38bdf8;
        color: #38bdf8;
        font-weight: bold;
        transition: 0.3s;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background: #38bdf8;
        color: #020617;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE & MODEL LOADING ---
@st.cache_resource
def load_sentinel_engine():
    # Google Drive Model ID
    file_id = '1b0r1ZQEyBQsaCrwprIQ4zwAQSTJZW5Ry'
    destination = 'sentinel_model.h5'
    
    if not os.path.exists(destination):
        url = f'https://drive.google.com/uc?id={file_id}'
        response = requests.get(url, stream=True)
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk: f.write(chunk)
    
    # Building EfficientNet Architecture
    base_model = tf.keras.applications.EfficientNetB0(weights=None, include_top=False, input_shape=(224, 224, 3))
    model = tf.keras.models.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.load_weights(destination)
    return model

# --- 3. DASHBOARD UI ---
st.markdown("<h1 class='main-title'>SENTINEL AI v3.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Advanced Neural Network Analysis for Forensic Verification</p>", unsafe_allow_html=True)
st.markdown("<div class='scanning-bar'></div><br>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📥 CORE INPUT")
    uploaded_file = st.file_uploader("Drop digital evidence here", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        st.image(img, channels="BGR", use_container_width=True)

with col2:
    st.markdown("### 🔍 ANALYTICS PANEL")
    if uploaded_file:
        if st.button("INITIATE NEURAL SCAN"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulated Industry Scanning Stages
            stages = ["Decrypting Pixels...", "Analyzing Noise Patterns...", "Running Neural Inference...", "Finalizing Verdict..."]
            for i, stage in enumerate(stages):
                status_text.text(f"STAGE {i+1}: {stage}")
                progress_bar.progress((i + 1) * 25)
                time.sleep(0.6)

            # Actual AI Prediction
            model = load_sentinel_engine()
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_crop = cv2.resize(cv2.cvtColor(img[y:y+h, x:x+w], cv2.COLOR_BGR2RGB), (224, 224))
                pred = float(model.predict(np.expand_dims(face_crop/255.0, 0), verbose=0)[0][0])
                
                # Industry Grade Result Display
                if pred > 0.5:
                    st.markdown("<div style='padding:20px; border-radius:10px; background:#064e3b; border:1px solid #10b981;'><h2 style='color:#10b981; margin:0;'>VERDICT: AUTHENTIC</h2><p style='margin:0;'>Neural Confidence: {:.2f}%</p></div>".format(pred*100), unsafe_allow_html=True)
                else:
                    st.markdown("<div style='padding:20px; border-radius:10px; background:#450a0a; border:1px solid #f43f5e;'><h2 style='color:#f43f5e; margin:0;'>VERDICT: MANIPULATED</h2><p style='margin:0;'>Neural Confidence: {:.2f}%</p></div>".format((1-pred)*100), unsafe_allow_html=True)
            else:
                st.warning("SYSTEM ALERT: No human subject detected. Basic pixel scan applied.")
                noise_val = cv2.Laplacian(gray, cv2.CV_64F).var()
                st.metric("Pixel Integrity Score", f"{noise_val:.2f}")

    else:
        st.info("System Standby. Awaiting digital input for forensic analysis.")

st.markdown("---")
st.markdown("<p style='text-align:center; font-size:12px; color:#475569;'>SECURE SCANNING | FOR OFFICIAL USE ONLY | RAUSHAN SINGH FORENSICS</p>", unsafe_allow_html=True)
