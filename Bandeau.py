import streamlit as st
import pandas as pd

def afficher_bandeau_covers(df_items):
    # 1. On récupère les URLs des couvertures (on enlève les lignes vides)
    # On limite à 20 livres pour que ce soit fluide
    covers_raw = df_items[df_items['api_thumbnail'].notna()]['api_thumbnail'].head(20).tolist()
    
    if not covers_raw:
        return 

    # 2. Nettoyage et Boost de résolution avec vérification de type
    covers = []
    for url in covers_raw:
        if isinstance(url, str): # On vérifie que c'est bien du texte
            new_url = url.replace('&zoom=1', '&zoom=2').replace('http://', 'https://')
            covers.append(new_url)




            

    # 2. Construction du HTML pour le défilement
    # On double la liste pour créer un effet de boucle infinie sans coupure
    img_tags = "".join([f'<img src="{url}" style="height:400px; width:280px;object-fit:cover; margin: 0 10px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">' for url in covers + covers])

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
    