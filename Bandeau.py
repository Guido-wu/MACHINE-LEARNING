import streamlit as st
import pandas as pd

def afficher_bandeau_covers(df_items):
    # 1. On récupère les URLs et on s'assure qu'elles ne sont pas vides
    covers_raw = df_items[df_items['api_thumbnail'].notna()]['api_thumbnail'].head(30).tolist()
    
    if not covers_raw:
        return 

    # Image de remplacement si la cover est cassée (un beau livre générique)
    placeholder = "https://images.unsplash.com/photo-1543004218-ee141104975a?q=80&w=280&h=400&auto=format&fit=crop"

    covers = []
    for url in covers_raw:
        if isinstance(url, str) and url.strip() != "":
            # On boost la résolution
            new_url = url.replace('&zoom=1', '&zoom=2').replace('http://', 'https://')
            covers.append(new_url)

    # 2. Construction du HTML
    # L'astuce ici : onerror="this.src='{placeholder}'" 
    # Si l'image ne charge pas, le navigateur la remplace par le placeholder
    img_tags = "".join([
        f'<img src="{url}" onerror="this.onerror=null;this.src=\'{placeholder}\';" '
        f'style="height:400px; width:280px; object-fit:cover; margin: 0 15px; '
        f'border-radius:15px; box-shadow: 0px 10px 20px rgba(0,0,0,0.3);">' 
        for url in covers + covers
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