import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import re
import base64

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="Pokémon Discovery", layout="wide")

st.markdown("""
    <style>
    /* Force all text to white */
    html, body, [data-testid="stWidgetLabel"], .stApp, p, h1, h2, h3, span, div { 
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
        font-size: 4.5em; 
        font-weight: 900; 
        text-align: center; 
        text-transform: uppercase; 
        letter-spacing: -1px; 
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    /* The White Circle Container */
    .img-circle {
        background-color: white;
        border-radius: 50%;
        width: 450px; 
        height: 450px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        border: 4px solid #444;
        overflow: hidden;
    }
    
    .img-circle img {
        max-width: 85%;
        max-height: 85%;
        object-fit: contain;
    }

    /* Slider Thickness & Alignment */
    .stSlider [data-baseweb="slider"] {
        height: 25px !important; 
    }
    
    .stSlider [data-baseweb="thumb"] {
        top: 5px !important; 
        width: 25px !important;
        height: 25px !important;
    }

    /* Nuke thumb values and keep tick bars invisible */
    div[data-testid="stThumbValue"] { display: none !important; }
    div[data-testid="stTickBar"] > div { color: transparent !important; }

    /* Text Styling */
    .side-label, .traits-title, .pretty-label {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .side-label { margin-top: 15px; }
    .traits-title { text-align: center; margin-bottom: 30px; }
    .pretty-label { text-align: center; margin-bottom: 10px; margin-top: 30px; }

    /* HARD CENTERING for Checkbox */
    /* This targets the specific div Streamlit uses for checkboxes */
    [data-testid="stCheckbox"] {
        display: flex;
        justify-content: center;
        width: 100% !important;
        padding-left: 0px;
    }
    /* Removes the internal padding that offsets the box to the left */
    [data-testid="stCheckbox"] > label {
        margin-left: auto;
        margin-right: auto;
        padding-left: 0px !important;
    }
    
    /* Style the Button */
    .stButton button {
        background-color: #333 !important;
        border-radius: 25px !important;
        padding: 12px 40px !important;
        border: 1px solid #555 !important;
        font-weight: bold;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOAD & HELPERS ---
@st.cache_data
def load_data():
    return pd.read_csv('top_10_pokemon_mappings.csv')

df_maps = load_data()

def get_image_html(image_path, ext):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    return f'''
        <div class="img-circle">
            <img src="data:image/{ext};base64,{encoded_string}">
        </div>
    '''

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

for i in range(1, 5):
    if f's{i}' not in st.session_state: st.session_state[f's{i}'] = 3
if 's5_check' not in st.session_state: st.session_state.s5_check = False

def randomize_traits():
    st.session_state.s1 = random.randint(1, 5)
    st.session_state.s2 = random.randint(1, 5)
    st.session_state.s3 = random.randint(1, 5)
    st.session_state.s4 = random.randint(1, 5)
    st.session_state.s5_check = random.choice([True, False])

# --- 4. UI LAYOUT ---
st.markdown("<h1 style='text-align:center; font-weight:200; letter-spacing:8px; margin-bottom:60px;'>POKÉMON DISCOVERY</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col2:
    # MOVE DOWN: Vertical spacer (approx 1 inch / 100px)
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 class='traits-title'>TRAITS</h2>", unsafe_allow_html=True)
    
    meta = df_maps[df_maps['combination'] == current_combo].iloc[0]
    attrs = [meta[f'attr{i}_name'] for i in range(1, 6)]
    
    def trait_row(label_pair, key):
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        l_col, m_col, r_col = st.columns([1.2, 3, 1.2])
        l_col.markdown(f"<p class='side-label' style='text-align:right;'>{label_pair[0]}</p>", unsafe_allow_html=True)
        with m_col:
            val = st.select_slider("", options=[1, 2, 3, 4, 5], key=key, label_visibility="collapsed")
        r_col.markdown(f"<p class='side-label' style='text-align:left;'>{label_pair[1]}</p>", unsafe_allow_html=True)
        return val

    v1 = trait_row(TRAIT_LABELS[attrs[0]], "s1")
    v2 = trait_row(TRAIT_LABELS[attrs[1]], "s2")
    v3 = trait_row(TRAIT_LABELS[attrs[2]], "s3")
    v4 = trait_row(TRAIT_LABELS[attrs[3]], "s4")
    
    # Pretty Section
    st.markdown("<p class='pretty-label'>PRETTY</p>", unsafe_allow_html=True)
    is_pretty = st.checkbox("", key="s5_check", label_visibility="collapsed")
    v5 = 4 if is_pretty else 2

    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        st.button('RANDOMIZE TRAITS', on_click=randomize_traits, use_container_width=True)

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
                html_block = get_image_html(img_path, ext)
                st.markdown(html_block, unsafe_allow_html=True)
                img_found = True
                break
        
        if not img_found:
            st.warning(f"Image for {p['pokeapi_name_fixed']} not found.")
    else:
        st.markdown("<div style='text-align:center; margin-top:200px;'><h2>No mapping found.</h2></div>", unsafe_allow_html=True)