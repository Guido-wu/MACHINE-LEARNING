import streamlit as st
import base64
import pandas as pd
import os
from item_to_reco import afficher_recommandations
from Bandeau import afficher_bandeau_covers
from Photo_Fond import afficher_image_fond, get_base64_of_bin_file
from Quote import afficher_quote_of_the_day
from top_books import afficher_top_books, afficher_new_releases
from my_library import afficher_my_library



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
        background-image: 
        linear-gradient(rgba(255, 248, 232, 0.75), rgba(255, 248, 232, 0.75)),
        url("data:image/png;base64,{get_base64_of_bin_file('Logo_2.png')}");
    background-repeat: no-repeat;
    background-position: center center;
    background-size: 600px;
    background-attachment: fixed;
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
    [data-testid="stSidebar"] label[data-baseweb="radio"] p {{
        font-family: 'Playfair Display', serif !important; /* La même que le titre */
        font-size: 1.3rem !important; /* Un peu plus grand pour l'élégance */
        color: white !important;
        font-weight: 500 !important;
        margin: 0 !important;
        padding-left: 10px !important;
    }}
    
    /* 3. Style pour l'image du logo */
    .logo-img {{
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 120px; /* Ajuste la taille ici */
        margin-bottom: 20px;
    }}


    /* Configuration de l'image de fond en haut à droite */
    .background-logo {{
        position: fixed;
        top: 20px;       /* Distance du haut */
        right: 20px;     /* Distance de la droite */
        width: 300px;    /* Taille de l'image */
        opacity: 0.1;    /* Transparence (0.1 = très transparent, 1.0 = opaque) */
        z-index: -1;     /* Place l'image DERRIÈRE le texte */
        pointer-events: none; /* Permet de cliquer sur les boutons à travers l'image */
    }}
    <style>




    /* Creation des boutons sidebar */
    




    /* Cache l'input radio physique */
    [data-testid="stSidebar"] input[type="radio"] {{
        display: none !important;
    }}
    
    /* Cible spécifiquement le cercle rouge/blanc de Streamlit */
    [data-testid="stSidebar"] div[data-baseweb="radio"] > div {{
        display: none !important;
        background-color: transparent !important;
    }}

    /* Cache le cercle blanc/rouge de Streamlit */
    div[data-testid="stWidgetLabel"] + div div[data-bv-test="radio-button"] {{
        display: none !important;
    }}
    
    /* 2. CRÉATION DU BOUTON SOBRE */
    div[role="radiogroup"] label {{
        background-color: transparent !important; /* Fond transparent par défaut */
        border-radius: 12px !important;
        padding: 12px 20px !important;
        margin-bottom: 8px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        align-items: center !important;
        border: none !important;
    }}

    /* 3. EFFET AU SURVOL (HOVER) */
    div[role="radiogroup"] label:hover {{
        background-color: rgba(255, 255, 255, 0.1) !important;
    }}

    /* 4. L'ÉLÉMENT SÉLECTIONNÉ RESTE CLAIR (ACTIVE) */
    /* On cible le label qui contient l'input coché */
    div[role="radiogroup"] label:has(input:checked) {{
        background-color: rgba(255, 255, 255, 0.2) !important; /* Reste plus clair */
        border-left: 4px solid white !important; /* Petit trait blanc pour marquer la position */
    }}
    
    /* On force la couleur du texte en blanc */
    div[role="radiogroup"] p {{
        color: white !important;
        font-size: 1.1rem !important;
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



# 3. CHARGEMENT DES DONNÉES et image de fond

@st.cache_data
def load_data():
    df_items = pd.read_csv("items.csv")
    df_reco = pd.read_csv("final_submission-2.csv")
    df_enriched = pd.read_csv("items_enriched_api.csv")
    df_quotes = pd.read_csv("quotes.csv")
    df_interactions = pd.read_csv("interactions_train.csv")
    df_categories = pd.read_csv("items_with_categories.csv")
    return df_items, df_reco, df_enriched, df_quotes, df_interactions, df_categories

df_items, df_reco, df_enriched, df_quotes, df_interactions, df_categories = load_data()




# 4. SIDEBAR (MENU DE GAUCHE)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-bottom: 0;'>The Bookworm</h1>", unsafe_allow_html=True)

    st.markdown("<p style='color:white; font-weight:bold; opacity:0.8;'>MENU</p>", unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        ["Home", "My Library", "Recommendations", "Statistics"],
        index=0,
        label_visibility="collapsed"
    )

    st.image("Logo_1.png", width=250) 

    st.markdown("<p style='font-style: italic; margin-top: 10px;'>Dive into stories. Grow your world</p>", unsafe_allow_html=True)
    st.markdown("---")
    


# 5. CONTENU PRINCIPAL - Chaque page de notre site 

if menu == "Home":

    st.markdown("<h1 style='color: #1a1a1a;'>Welcome to The Bookworm</h1>", unsafe_allow_html=True)


    st.divider()
    col1, col2 = st.columns([1,1.5])

    with col1:
        st.markdown("""<div class="book-card"><h3 style="color:#1f6f43;">🏆 Top Books</h3></div>""", unsafe_allow_html=True)
        afficher_top_books(df_enriched, df_interactions)

    with col2:
        st.markdown("""<div class="book-card"><h3 style="color:#1f6f43;">✨ New Releases</h3></div>""", unsafe_allow_html=True)
        afficher_new_releases(df_enriched)




    st.divider()
    col1, col2 = st.columns([2,1])

    with col1:
        
        afficher_quote_of_the_day(df_quotes)

    with col2:
        st.image("Logo_3.png", width=250) 




    # Ton bandeau défilant (Resolution Boosted)
    afficher_bandeau_covers(df_enriched)










elif menu == "Recommendations":
      
    user_id = st.number_input("Enter User ID :", min_value=0, max_value=len(df_reco)-1, step=1)
    if st.button("Get Recommendations"):
        afficher_recommandations(user_id, df_reco, df_items)



elif menu == "My Library":
    
    st.title("My Library")
    st.dataframe(df_items.head(50)) # Exemple d'affichage



elif menu == "Statistics":
    
    st.title("Reading Insights")
    # Petit graph simple pour le look
    chart_data = pd.DataFrame([10, 15, 30, 20, 5, 25], index=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
    st.bar_chart(chart_data)
