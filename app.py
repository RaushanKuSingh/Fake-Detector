import streamlit as st
import cv2
import numpy as np
import os
import time
import tensorflow as tf
import requests

# --- 1. Google Drive Model Downloader ---
@st.cache_resource
def download_model_from_drive():
    file_id = '1b0r1ZQEyBQsaCrwprIQ4zwAQSTJZW5Ry'
    destination = 'deepfake_industry_weights.weights.h5'
    if not os.path.exists(destination):
        with st.spinner("🚀 Initializing Enterprise AI Core..."):
            url = f'https://drive.google.com/uc?id={file_id}'
            response = requests.get(url, stream=True)
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk: f.write(chunk)
    return destination

# --- 2. Elite UI Setup ---
st.set_page_config(page_title="Fake Detector Pro", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #1e293b, #0f172a, #020617); color: #f8fafc; }
    .hero-container { text-align: center; padding: 20px 0; }
    .hero-title { font-size: 3.5rem; font-weight: 900; background: linear-gradient(to bottom, #ffffff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; margin-bottom: 10px;}
    div[data-testid="stFileUploader"] section { padding: 25px !important; border-radius: 25px; background: rgba(255, 255, 255, 0.02); border: 2px solid rgba(56, 189, 248, 0.2); }
    div[data-testid="stFileUploader"] section > div:nth-child(1) { display: none; }
    .stButton>button { width: 100%; height: 65px; border-radius: 15px; background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%); color: white; font-size: 22px !important; font-weight: 800; text-transform: uppercase; box-shadow: 0 10px 30px rgba(37, 99, 235, 0.3); }
    .block-container { padding-top: 1.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Backend Engine ---
@st.cache_resource
def load_core():
    try:
        weights_path = download_model_from_drive()
        base = tf.keras.applications.EfficientNetB0(weights=None, include_top=False, input_shape=(224, 224, 3))
        m = tf.keras.models.Sequential([
            base,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        if os.path.exists(weights_path):
            m.load_weights(weights_path)
            return m
    except Exception: return None
    return None

model = load_core()

# --- 4. UI Header ---
st.markdown("<div class='hero-container'><h1 class='hero-title'>FAKE DETECTOR</h1></div>", unsafe_allow_html=True)

# Central Upload logic using Session State to avoid buffer re-reading
if 'uploaded_data' not in st.session_state:
    c1, c2, c3 = st.columns([1, 3, 1])
    with c2:
        uploaded_file = st.file_uploader(" ", type=["jpg", "png", "jpeg"], key="main_uploader")
        if uploaded_file:
            st.session_state['uploaded_data'] = uploaded_file.read() # Read ONLY once
            st.rerun()

# After Upload View
if 'uploaded_data' in st.session_state:
    img_bytes = st.session_state['uploaded_data']
    img_cv = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), 1)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    
    col_img, col_action, col_res = st.columns([1.2, 1.3, 1.2], gap="medium")
    
    with col_img:
        st.markdown("##### 📸 EVIDENCE")
        st.image(img_rgb, use_container_width=True)
        if st.button("🔄 CLEAR"):
            del st.session_state['uploaded_data']
            st.rerun()

    with col_action:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚀 EXECUTE SCAN"):
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            noise_val = cv2.Laplacian(gray, cv2.CV_64F).var()
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            with col_res:
                st.markdown("##### 📊 VERDICT")
                if len(faces) > 0 and model:
                    x,y,w,h = faces[0]
                    face = cv2.resize(img_rgb[y:y+h, x:x+w], (224, 224))
                    pred = float(model.predict(np.expand_dims(face/255.0, 0), verbose=0)[0][0])
                    is_real = (noise_val > 65 and pred > 0.45) or (pred > 0.85)
                    
                    if is_real: st.success(f"REAL | {pred*100:.1f}%")
                    else: st.error(f"FAKE | {(1-pred)*100:.1f}%")
                    st.image(face, width=120)
                else:
                    if noise_val < 45: st.error("FAKE OBJECT")
                    else: st.success("REAL OBJECT")
                st.metric("INTEGRITY", f"{noise_val:.1f}")