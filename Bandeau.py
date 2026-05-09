import streamlit as st
import pandas as pd
import base64

# --- 1. DÉFINITION DE LA FONCTION (Tout en haut !) ---
def afficher_bandeau_covers(df_items):
    # On prend les thumbnails non vides
    covers = df_items[df_items['api_thumbnail'].notna()]['api_thumbnail'].head(20).tolist()
    if not covers:
        return 
    
    img_tags = "".join([f'<img src="{url}" style="height:200px; margin: 0 10px; border-radius:10px;">' for url in covers + covers])
    
    scroll_html = f"""
    <div style="overflow: hidden; white-space: nowrap; width: 100%;">
        <div style="display: inline-block; animation: scroll 40s linear infinite;">
            {img_tags}
        </div>
    </div>
    <style>
    @keyframes scroll {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-50%); }} }}
    </style>
    """
    st.markdown(scroll_html, unsafe_allow_html=True)

# --- 2. CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    df_items = pd.read_csv("items.csv")
    df_reco = pd.read_csv("final_submission-2.csv")
    df_enriched = pd.read_csv("items_enriched_api.csv") # Ton nouveau fichier
    return df_items, df_reco, df_enriched

df_items, df_reco, df_enriched = load_data()
