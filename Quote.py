import streamlit as st
import pandas as pd
from datetime import date

def afficher_quote_of_the_day(df_quotes):
    day_of_year = date.today().timetuple().tm_yday
    total = len(df_quotes)

    if "quote_offset" not in st.session_state:
        st.session_state.quote_offset = 0
    if "quote_direction" not in st.session_state:
        st.session_state.quote_direction = "next"

    idx = (day_of_year + st.session_state.quote_offset) % total
    row = df_quotes.iloc[idx]

    # Direction de l'animation selon le bouton cliqué
    anim_from = "60px" if st.session_state.quote_direction == "next" else "-60px"

    st.markdown(f"""
        <style>
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateX({anim_from});
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        .quote-card {{
            background-color: #FFFFFF;
            padding: 35px 40px;
            border-radius: 20px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.07);
            border-left: 6px solid #1f6f43;
            animation: slideIn 0.45s ease;
            position: relative;
            margin-bottom: 15px;
        }}

        .quote-icon {{
            font-size: 4rem;
            color: #1f6f43;
            opacity: 0.15;
            position: absolute;
            top: 10px;
            right: 25px;
            font-family: Georgia, serif;
            line-height: 1;
        }}

        .quote-text {{
            font-style: italic;
            font-size: 1.15rem;
            color: #2c2c2c;
            line-height: 1.7;
            margin-bottom: 15px;
            font-family: 'Lora', Georgia, serif;
        }}

        .quote-author {{
            text-align: right;
            color: #1f6f43;
            font-weight: bold;
            font-size: 0.95rem;
            font-family: 'Playfair Display', serif;
        }}

        .quote-counter {{
            text-align: center;
            color: #aaa;
            font-size: 0.8rem;
            margin-top: 5px;
            margin-bottom: 10px;
        }}

        .stButton > button {{
            border-radius: 30px !important;
            border: 2px solid #1f6f43 !important;
            color: #1f6f43 !important;
            background-color: transparent !important;
            font-weight: 600 !important;
            padding: 8px 24px !important;
            transition: all 0.2s ease !important;
        }}
        .stButton > button:hover {{
            background-color: #1f6f43 !important;
            color: white !important;
        }}
        </style>

        <div class="quote-card">
            <span class="quote-icon">"</span>
            <p class="quote-text">"{row['quote']}"</p>
            <p class="quote-author">— {row['author']}</p>
        </div>
        <p class="quote-counter">✦ Quote {idx + 1} of {total} ✦</p>
    """, unsafe_allow_html=True)

    # Boutons Previous / Next centrés
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Previous"):
            st.session_state.quote_offset -= 1
            st.session_state.quote_direction = "prev"
            st.rerun()
    with col3:
        if st.button("Next →"):
            st.session_state.quote_offset += 1
            st.session_state.quote_direction = "next"
            st.rerun()