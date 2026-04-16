import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import re

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="Pokemon Discovery", layout="wide")

# Custom CSS for your specific requests
st.markdown("""
    <style>
    /* Dark Background */
    .main { background-color: #1a1a1a; color: white; }
    
    /* Center the Pokemon Name */
    .pkmn-name { 
        font-size: 3.5em; 
        font-weight: 900; 
        text-align: center; 
        text-transform: uppercase; 
        letter-spacing: -1px; 
        color: white; 
        margin-bottom: 10px;
    }
    
    /* Remove the Circle and center the image */
    .img-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        padding: 20px;
    }

    /* Make sliders thicker */
    .stSlider [data-baseweb="slider"] {
        height: 12px;
    }
    .stSlider [data-baseweb="slider"] div {
        height: 12px;
    }

    /* Hide the numbers (value) above the slider */
    .stSlider [data-testid="stWidgetLabel"] p {
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div[data-testid="stThumbValue"] {
        display: none;
    }
    
    /* Styling for the side labels */
    .side-label {
        font-size: 12px;
        font-weight: 700;
        color: #888;
        text-transform: uppercase;
        margin-top: 35px;
    }
    
    /* Center the button */
    .stButton {
        display: flex;
        justify-content: center;
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
# Since we removed the combo slider, we pick the first available combo as default
current_combo = df_maps['combination'].unique()[0]

# --- 4. UI LAYOUT ---
st.markdown("<h1 style='text-align:center; font-weight:200; letter-spacing:8px; margin-bottom:50px;'>POKEMON DISCOVERY</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col2:
    # Get current attribute names based on combo
    meta = df_maps[df_maps['combination'] == current_combo].iloc[0]
    attrs = [meta[f'attr{i}_name'] for i in range(1, 6)]
    
    # Initialize Session States for Randomization
    if 's1' not in st.session_state: st.session_state.s1 = 3
    if 's2' not in st.session_state: st.session_state.s2 = 3
    if 's3' not in st.session_state: st.session_state.s3 = 3
    if 's4' not in st.session_state: st.session_state.s4 = 3
    if 's5' not in st.session_state: st.session_state.s5 = 2

    # Sliders with side labels
    def trait_row(label_pair, key, is_select=False):
        l_col, m_col, r_col = st.columns([1, 3, 1])
        l_col.markdown(f"<p class='side-label' style='text-align:right;'>{label_pair[0]}</p>", unsafe_allow_html=True)
        with m_col:
            if is_select:
                val = st.select_slider("", options=[2, 4], key=key)
            else:
                val = st.slider("", 1, 5, key=key)
        r_col.markdown(f"<p class='side-label' style='text-align:left;'>{label_pair[1]}</p>", unsafe_allow_html=True)
        return val

    v1 = trait_row(TRAIT_LABELS[attrs[0]], "s1")
    v2 = trait_row(TRAIT_LABELS[attrs[1]], "s2")
    v3 = trait_row(TRAIT_LABELS[attrs[2]], "s3")
    v4 = trait_row(TRAIT_LABELS[attrs[3]], "s4")
    v5 = trait_row(TRAIT_LABELS[attrs[4]], "s5", is_select=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button('RANDOMIZE TRAITS'):
        st.session_state.s1 = random.randint(1, 5)
        st.session_state.s2 = random.randint(1, 5)
        st.session_state.s3 = random.randint(1, 5)
        st.session_state.s4 = random.randint(1, 5)
        st.session_state.s5 = random.choice([2, 4])
        st.rerun()

with col1:
    # --- MATCHING LOGIC ---
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
                st.markdown('<div class="img-container">', unsafe_allow_html=True)
                st.image(img_path, width=400)
                st.markdown('</div>', unsafe_allow_html=True)
                img_found = True
                break
        
        if not img_found:
            st.warning(f"Image for {p['pokeapi_name_fixed']} not found.")
    else:
        st.markdown("<div style='text-align:center; margin-top:100px;'><h2>No mapping found.</h2></div>", unsafe_allow_html=True)