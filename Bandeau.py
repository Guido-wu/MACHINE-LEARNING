import streamlit as st
import pandas as pd

def afficher_bandeau_covers(df_items):
    # 1. On récupère les URLs des couvertures (on enlève les lignes vides)
    # On limite à 20 livres pour que ce soit fluide
    covers = df_items[df_items['api_thumbnail'].notna()]['api_thumbnail'].head(20).tolist()
    
    if not covers:
        return # Si aucune image n'est trouvée, on n'affiche rien

    # 2. Construction du HTML pour le défilement
    # On double la liste pour créer un effet de boucle infinie sans coupure
    img_tags = "".join([f'<img src="{url}" style="height:200px; margin: 0 10px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">' for url in covers + covers])

    scroll_html = f"""
    <div style="overflow: hidden; white-space: nowrap; width: 100%; background: rgba(255,255,255,0.1); padding: 10px 0;">
        <div style="display: inline-block; animation: scroll 40s linear infinite;">
            {img_tags}
        </div>
    </div>

    <style>
    @keyframes scroll {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-50%); }}
    }}
    </style>
    """
    
    st.markdown(scroll_html, unsafe_allow_html=True)
    