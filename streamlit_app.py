import streamlit as st
import base64
import pandas as pd
import os
from item_to_reco import afficher_recommandations
from Bandeau import afficher_bandeau_covers



# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="The Bookworm",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. DESIGN CSS (Le "Beige" et le "Vert")
st.markdown(f"""
    <style>
    /* Fond principal en Beige */
    .stApp {{
        background-color: #fff8e8;
    }}

    /* Sidebar en Vert  */
    [data-testid="stSidebar"] {{
        background-color: #1f6f43;
    }}
    
    /* 1. On importe la police depuis Google */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lora:ital@0;1&display=swap');

    /* Texte de la sidebar en blanc */
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {{
        color: #FFFFFF !important;
    }}


    /* 2. On l'applique à la Sidebar */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] label {{ 
        color: #FFFFFF !important;
        font-family: 'Playfair Display', serif !important; /* La police Fancy */
        font-size: 1.1rem;
    }}
    
    /* 3. Style pour l'image du logo */
    .logo-img {{
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 120px; /* Ajuste la taille ici */
        margin-bottom: 20px;
    }}

    <style>
    /* 1. On cache les petits ronds (radio buttons) */
    [data-testid="stSidebarNavLink"] div:has(input) {{
        display: none !important;
    }}
    
    /* 2. On transforme chaque option du menu en gros bouton élégant */
    [data-testid="stSidebarNav"] li {{
        background-color: transparent;
        border-radius: 15px;
        margin-bottom: 5px;
        transition: all 0.3s ease;
    }}  

    /* 3. Effet quand on passe la souris dessus (Hover) */
    [data-testid="stSidebarNav"] li:hover {{
        background-color: rgba(255, 255, 255, 0.1); /* Couleur plus claire au survol */
        transform: translateX(5px); /* Petit mouvement vers la droite */
    }}

    /* 4. Style de l'option sélectionnée (comme sur votre image d'inspi) */
    [data-testid="stSidebarNav"] li:has(a[aria-current="page"]) {{
        background-color: #3e8e5d !important; /* Vert plus clair pour l'actif */
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}

    /* 5. On ajuste le texte à l'intérieur */
    [data-testid="stSidebarNav"] a {{
        color: white !important;
        font-family: 'Lora', serif !important;
        font-size: 1.1rem !important;
        text-decoration: none !important;
        padding: 10px 15px !important;
    }}
    

    /* Style des cartes blanches */
    .book-card {{
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. CHARGEMENT DES DONNÉES
@st.cache_data
def load_data():
    df_items = pd.read_csv("items.csv")
    df_reco = pd.read_csv("final_submission-2.csv")
    df_enriched = pd.read_csv("items_enriched_api.csv")
    return df_items, df_reco, df_enriched

df_items, df_reco, df_enriched = load_data()

# 4. SIDEBAR (MENU DE GAUCHE)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-bottom: 0;'>The Bookworm</h1>", unsafe_allow_html=True)

    st.image("Logo_1.png", width=250) 

    st.markdown("<p style='font-style: italic; margin-top: 10px;'>Dive into stories. Grow your world</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<p style='color:white; font-weight:bold; opacity:0.8;'>NAVIGATION</p>", unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        ["🏠 Home", "📚 My Library", "✨ Recommendations", "📊 Statistics"],
        index=0,
        label_visibility="collapsed"
    )
    st.markdown("---")
    








# 5. CONTENU PRINCIPAL - Chaque page de notre site 
if menu == "🏠 Home":

    st.markdown("<h1 style='color: #1a1a1a;'>Welcome to The Bookworm</h1>", unsafe_allow_html=True)
    
    # Ton bandeau défilant (Resolution Boosted)
    afficher_bandeau_covers(df_enriched)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="book-card">
                <h3 style="color: #1f6f43;">New user - Recommandation</h3>
                <p>Find your next favorite book based on your reading history.</p>
            </div>
        """, unsafe_allow_html=True)
        
        user_id = st.number_input("Enter User ID :", min_value=0, max_value=len(df_reco)-1, step=1)
        if st.button("Get Recommendations"):
            afficher_recommandations(user_id, df_reco, df_items)

    with col2:
        st.markdown("""
            <div class="book-card">
                <h3 style="color: #1f6f43;">Reading Goals 2025</h3>
                <p>You have read <b>24</b> books out of 50.</p>
            </div>
        """, unsafe_allow_html=True)
        st.progress(0.48)

elif menu == "📚 My Library":
    st.title("My Library")
    st.dataframe(df_items.head(50)) # Exemple d'affichage

elif menu == "📊 Statistics":
    st.title("Reading Insights")
    # Petit graph simple pour le look
    chart_data = pd.DataFrame([10, 15, 30, 20, 5, 25], index=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
    st.bar_chart(chart_data)
