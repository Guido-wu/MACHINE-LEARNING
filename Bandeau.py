import streamlit as st
import pandas as pd

def afficher_bandeau_covers(df_items):
    # 1. On filtre drastiquement : pas de NaN et on s'assure que c'est du texte
    # On en prend 50 au départ pour être sûr d'en avoir au moins 20 valides à l'arrivée
    potential_covers = df_items[df_items['api_thumbnail'].notna()]['api_thumbnail'].head(50).tolist()
    
    covers = []
    for url in potential_covers:
        if isinstance(url, str) and len(url) > 10: # On vérifie que l'URL a une longueur crédible
            # Boost de résolution
            clean_url = url.replace('&zoom=1', '&zoom=2').replace('http://', 'https://')
            covers.append(clean_url)
    
    # On ne garde que les 20 premières valides pour la fluidité
    final_covers = covers[:20]

    if not final_covers:
        return 

    # 2. Construction du HTML
    # On n'affiche QUE les images qui ont réussi le filtre
    img_tags = "".join([
        f'<img src="{u}" style="height:400px; width:280px; object-fit:cover; margin: 0 15px; border-radius:15px; box-shadow: 0px 10px 20px rgba(0,0,0,0.3);">' 
        for u in final_covers + final_covers
    ])

    scroll_html = f"""
    <div style="overflow: hidden; white-space: nowrap; width: 100%; height: 450px; display: flex; align-items: center;">
        <div style="display: inline-block; animation: scroll 60s linear infinite;">
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