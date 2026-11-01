import os
import json
import base64
from pathlib import Path
import streamlit as st
import pandas as pd
from data_cleaning import clean_mobile_data
from recommendation import PERSONA_WEIGHTS

# Paths & Branding
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
LOGO_PATH = ROOT_DIR / "assets" / "logo.png"
FAVICON_PATH = ROOT_DIR / "assets" / "favicon.png"
TEMPLATE_PATH = BASE_DIR / "frontend_template.html"

# Page Config
st.set_page_config(
    page_title="SmartPick AI | Live Deployment",
    page_icon="📱",
    layout="wide"
)

def get_data_uri(path):
    if not path.exists(): return ""
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()

@st.cache_data
def get_live_data():
    """Loads and cleans the live dataset using the Python ML backend."""
    df = clean_mobile_data(str(ROOT_DIR / 'datasets' / 'sic_mobile_spec_PJ1.xlsx'))
    
    # Custom scoring for Display Types to match Modern UI logic
    DISPLAY_SCORE = {'AMOLED': 4.0, 'HD+ AMOLED': 5.0, 'LCD': 2.5, 'TFT': 1.5}
    
    records = [{
        'name': r['name'],
        'brand': str(r['name']).split()[0],
        'clean_price': float(r['price']),
        'camera': int(r['camera']),
        'clean_display_type': r['display_type'],
        'display_size': float(r['display_size']),
        'battery': int(r['battery']),
        'clean_storage': int(r['storage_gb']),
        'ram': int(r['ram']),
        'weight': float(r['weight']),
        'clean_processor': r['processor_cleaned'],
        'rating': float(r['rating']),
        'display_score': DISPLAY_SCORE.get(r['display_type'], 2.0),
        'processor_score': float(r['processor_score']),
    } for _, r in df.iterrows()]
    
    # Map Python weights to JS criteria names
    KEY_MAP = {'storage_gb': 'storage', 'processor_score': 'processor'}
    weights = {p: {KEY_MAP.get(k, k): v for k, v in w.items()} for p, w in PERSONA_WEIGHTS.items()}
    
    return records, weights

# Build the Dynamic UI
try:
    records, weights = get_live_data()
    
    if TEMPLATE_PATH.exists():
        html_content = TEMPLATE_PATH.read_text(encoding='utf-8')
        
        # Inject Python Logic into Modern UI
        html_content = (html_content
            .replace('__DATA__', json.dumps(records))
            .replace('__WEIGHTS__', json.dumps(weights))
            .replace('__LOGO__', get_data_uri(LOGO_PATH))
            .replace('__FAVICON__', get_data_uri(FAVICON_PATH))
        )
        
        # Render the Modern Frontend inside Streamlit
        st.components.v1.html(html_content, height=1200, scrolling=True)
        
    else:
        st.error("Frontend template not found. Please ensure 'frontend_template.html' exists in the notebooks folder.")

except Exception as e:
    st.error(f"Error initializing SmartPick AI: {str(e)}")

# Hidden Streamlit elements to keep the UI clean
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0px;}
    iframe {border: none;}
    </style>
""", unsafe_allow_html=True)