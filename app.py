import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import re

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="Pokemon Trait Mapper", layout="wide")

# Custom CSS to mimic your dark notebook theme
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: white; }
    .stSlider label { color: white !important; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .pkmn-name { font-size: 3em; font-weight: 900; text-align: center; text-transform: uppercase; letter-spacing: -1px; color: white; margin-top: -20px;}
    .img-container {
        background: white; border-radius: 50%; border: 3px solid #444;
        display: flex; align-items: center; justify-content: center;
        width: 350px; height: 350px; margin: 0 auto;
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

# --- 3. UI LAYOUT ---
st.markdown("<h2 style='text-align:center; font-weight:200; letter-spacing:5px;'>TRAIT-TO-POKÉMON MAPPER</h2>", unsafe_allow_html=True)

# Top Selection Slider
combo_options = df_maps['combination'].unique().tolist()
current_combo = st.select_slider('TOP 10 COMBOS', options=combo_options)

# Layout Columns
col1, col2 = st.columns([1, 1])

with col2:
    # Get current attribute names based on combo
    meta = df_maps[df_maps['combination'] == current_combo].iloc[0]
    attrs = [meta[f'attr{i}_name'] for i in range(1, 6)]
    
    # Create Sliders
    # Note: Streamlit doesn't have a "Randomize" button that works exactly like ipywidgets 
    # without a page rerun, so we use a button to reset session state if needed.
    if st.button('RANDOMIZE TRAITS'):
        st.session_state.s1 = random.randint(1, 5)
        st.session_state.s2 = random.randint(1, 5)
        st.session_state.s3 = random.randint(1, 5)
        st.session_state.s4 = random.randint(1, 5)
        st.session_state.s5 = random.choice([2, 4])

    v1 = st.slider(f"{TRAIT_LABELS[attrs[0]][0]} — {TRAIT_LABELS[attrs[0]][1]}", 1, 5, key="s1")
    v2 = st.slider(f"{TRAIT_LABELS[attrs[1]][0]} — {TRAIT_LABELS[attrs[1]][1]}", 1, 5, key="s2")
    v3 = st.slider(f"{TRAIT_LABELS[attrs[2]][0]} — {TRAIT_LABELS[attrs[2]][1]}", 1, 5, key="s3")
    v4 = st.slider(f"{TRAIT_LABELS[attrs[3]][0]} — {TRAIT_LABELS[attrs[3]][1]}", 1, 5, key="s4")
    v5 = st.select_slider(f"{TRAIT_LABELS[attrs[4]][0]} — {TRAIT_LABELS[attrs[4]][1]}", options=[2, 4], key="s5")

with col1:
    # --- LOGIC ---
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
        
        # Image Search logic
        img_found = False
        for ext in ['png', 'jpg', 'jpeg', 'webp']:
            img_path = f"pokemon_artwork/{p['pokeapi_name_fixed']}.{ext}"
            if os.path.exists(img_path):
                st.markdown(f'<div class="img-container">', unsafe_allow_html=True)
                st.image(img_path, use_column_width=False, width=300)
                st.markdown('</div>', unsafe_allow_html=True)
                img_found = True
                break
        
        if not img_found:
            st.warning(f"Image for {p['pokeapi_name_fixed']} not found in folder.")
    else:
        st.markdown("<div style='text-align:center;'><h2>No mapping found.</h2></div>", unsafe_allow_html=True)