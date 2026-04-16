import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import re

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="Pokémon Discovery", layout="wide")

# Custom CSS for your specific layout requests
st.markdown("""
    <style>
    /* Force all text to white */
    html, body, [data-testid="stWidgetLabel"], .stApp, p, h1, h2, h3 { 
        color: white !important; 
    }
    
    /* Dark Background */
    .stApp { background-color: #1a1a1a; }
    
    /* Remove the 'link' icon next to headers */
    .stApp [data-testid="stHeaderActionElements"],
    button[data-testid="baseLinkButton"],
    a.anchor-link { display: none !important; }

    /* Pokémon Name Styling */
    .pkmn-name { 
        font-size: 3.5em; 
        font-weight: 900; 
        text-align: center; 
        text-transform: uppercase; 
        letter-spacing: -1px; 
        margin-top: 20px;
    }
    
    /* The White Circle Container */
    .img-circle {
        background-color: white;
        border-radius: 50%;
        width: 400px;
        height: 400px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        border: 4px solid #444;
        overflow: hidden;
    }
    
    /* Ensure the image inside the circle looks correct */
    .img-circle img {
        max-width: 80% !important;
        height: auto !important;
    }

    /* Slider Thickness & Alignment */
    .stSlider [data-baseweb="slider"] {
        height: 25px !important; /* Even thicker */
    }
    
    /* Center the slider thumb (handle) */
    .stSlider [data-baseweb="thumb"] {
        top: 5px !important; 
        width: 25px !important;
        height: 25px !important;
    }

    /* Aggressive Hiding of numbers and labels */
    [data-testid="stWidgetLabel"], 
    [data-testid="stThumbValue"], 
    [data-testid="stSliderTickBar"],
    .st-at, .st-ae { 
        display: none !important; 
    }
    
    /* Side labels leveled with the thick slider */
    .side-label {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 18px; 
    }
    
    /* Centering the button with the column content */
    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 40px;
    }
    
    .stButton button {
        background-color: #333 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 12px 40px !important;
        border: 1px solid #555 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOAD ---
@st.cache_data
def load_data():
    return pd.read_csv('top_10_pokemon_mappings.csv')

df_maps = load_data()

TRAIT_LABELS = {
    'complexity': ('Simple', 'Complex'),
    'realism': ('Cartoony', 'Realistic'),
    'artificiality': ('Biological', 'Artificial'),
    'fantasy': ('Normal', 'Fantastical'),
    'humanoid': ('Not humanoid', 'Very humanoid'),
    'cuteness': ('Not cute', 'Very cute'),
    'coolness': ('Not cool', 'Very cool'),
    'beauty': ('Ugly', 'Pretty'),
    'popularity': ('Unpopular', 'Popular')
}

# --- 3. LOGIC & INITIALIZATION ---
current_combo = df_maps['combination'].unique()[0]

# Initialize Session States
for i in range(1, 5):
    if f's{i}' not in st.session_state: st.session_state[f's{i}'] = 3
if 's5' not in st.session_state: st.session_state.s5 = 2

# --- 4. UI LAYOUT ---
st.markdown("<h1 style='text-align:center; font-weight:200; letter-spacing:8px; margin-bottom:60px;'>POKÉMON DISCOVERY</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col2:
    meta = df_maps[df_maps['combination'] == current_combo].iloc[0]
    attrs = [meta[f'attr{i}_name'] for i in range(1, 6)]
    
    def trait_row(label_pair, key, is_select=False):
        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
        l_col, m_col, r_col = st.columns([1.2, 3, 1.2])
        l_col.markdown(f"<p class='side-label' style='text-align:right;'>{label_pair[0]}</p>", unsafe_allow_html=True)
        with m_col:
            if is_select:
                val = st.select_slider("", options=[2, 4], key=key, label_visibility="collapsed")
            else:
                val = st.slider("", 1, 5, key=key, label_visibility="collapsed")
        r_col.markdown(f"<p class='side-label' style='text-align:left;'>{label_pair[1]}</p>", unsafe_allow_html=True)
        return val

    v1 = trait_row(TRAIT_LABELS[attrs[0]], "s1")
    v2 = trait_row(TRAIT_LABELS[attrs[1]], "s2")
    v3 = trait_row(TRAIT_LABELS[attrs[2]], "s3")
    v4 = trait_row(TRAIT_LABELS[attrs[3]], "s4")
    v5 = trait_row(TRAIT_LABELS[attrs[4]], "s5", is_select=True)

    # The button is now nested inside this column to ensure centering with the sliders
    if st.button('RANDOMIZE TRAITS'):
        st.session_state.s1 = random.randint(1, 5)
        st.session_state.s2 = random.randint(1, 5)
        st.session_state.s3 = random.randint(1, 5)
        st.session_state.s4 = random.randint(1, 5)
        st.session_state.s5 = random.choice([2, 4])
        st.rerun()

with col1:
    match = df_maps[
        (df_maps['combination'] == current_combo) &
        (df_maps['attr1_val'] == v1) &
        (df_maps['attr2_val'] == v2) &
        (df_maps['attr3_val'] == v3) &
        (df_maps['attr4_val'] == v4) &
        (df_maps['attr5_val'] == v5)
    ]

    if not match.empty:
        p = match.iloc[0]
        clean_name = re.sub(r'(?i)standard\s*', '', p['pokemon']).strip('- ').title()
        st.markdown(f'<h1 class="pkmn-name">{clean_name}</h1>', unsafe_allow_html=True)
        
        img_found = False
        for ext in ['png', 'jpg', 'jpeg', 'webp']:
            img_path = f"pokemon_artwork/{p['pokeapi_name_fixed']}.{ext}"
            if os.path.exists(img_path):
                # FIXED IMAGE DISPLAY logic: One container, one image call.
                st.markdown('<div class="img-circle">', unsafe_allow_html=True)
                st.image(img_path, use_column_width=False, width=320)
                st.markdown('</div>', unsafe_allow_html=True)
                img_found = True
                break
        
        if not img_found:
            st.warning(f"Image for {p['pokeapi_name_fixed']} not found.")
    else:
        st.markdown("<div style='text-align:center; margin-top:150px;'><h2>No mapping found.</h2></div>", unsafe_allow_html=True)