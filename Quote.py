import streamlit as st
import pandas as pd
from datetime import date
 
def afficher_quote_of_the_day(df_quotes):
    # Calcule l'index du jour (change chaque jour automatiquement)
    day_of_year = date.today().timetuple().tm_yday  # 1 → 365
    total = len(df_quotes)
 
    # Initialise l'état de la citation courante dans la session
    if "quote_offset" not in st.session_state:
        st.session_state.quote_offset = 0
 
    # Index final = jour + offset (modulo pour boucler)
    idx = (day_of_year + st.session_state.quote_offset) % total
    row = df_quotes.iloc[idx]
 
    # Affichage de la carte
    st.markdown(f"""
        <div class="book-card">
            <h3 style="color: #1f6f43;">Quote of the Day</h3>
            <p style="font-style: italic; font-size: 1.1rem; color: #31333F;">
                "{row['quote']}"
            </p>
            <p style="text-align: right; color: #888; font-size: 0.9rem;">
                — {row['author']}
            </p>
        </div>
    """, unsafe_allow_html=True)
 
    # Boutons navigation
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Previous"):
            st.session_state.quote_offset -= 1
            st.rerun()
    with col2:
        if st.button("Next ➡️"):
            st.session_state.quote_offset += 1
            st.rerun()