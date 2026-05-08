import streamlit as st
import base64
import pandas as pd
import os




#Ajout d'un titre et d'un sous titre dans l'application 
st.set_page_config(
    page_title="Omega Book Recommendation",
    page_icon="📚",
    layout="wide"
)


#Ajout d'une image de background dans l'application
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


img_base64 = get_base64_of_bin_file('Biblio.jpeg')

st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), 
        url(https://mediatheques.haute-saone.fr/images/BDP70/Lire_Ecouter_Voir/Coups_de_coeur/2023/2023-01/2023-01-Coup-de-coeur-bibliotheques-DIAPO.jpg);
        background-attachment: fixed;
        background-size: cover;
        backdrop-filter: blur(5px); /* Ajoute un léger flou */
    }

    </style>
    """,

    unsafe_allow_html=True
)



# Style pour le titre et le sous-titre

st.markdown(
    """
    <div style="
        background-color: rgba(250, 249, 246, 0.85); 
        padding: 40px; 
        border-radius: 25px; 
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        margin: 20px auto;
        max-width: 800px;
    ">

    <h1 style='text-align: center; font-family: "Trebuchet MS", sans-serif; color: black;'>
        Welcome to our books recomendation app !!
    </h1>

    <p style='text-align: center; font-family: "Courier New", monospace; font-size: 20px;'>
    Find the book that fits you the best !
    </p>

    </div>
    """, 
    unsafe_allow_html=True
)




# ajout d'une flèche rebond pour notre bouton de scroll
for _ in range(20):
    st.write("")

st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <p style="font-size: 30px; animation: bounce 2s infinite;">↓</p>
    </div>
    <style>
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
        40% {transform: translateY(-10px);}
        60% {transform: translateY(-5px);}
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.divider()

#Creation d'une fonction bloc pour séparer les différentes sections de l'application

def bloc_style(titre, contenu):
    return f"""
    <div style="
        background-color: rgba(250, 249, 246, 0.85); 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0px 5px 15px rgba(0,0,0,0.08);
        text-align: center;
        height: 200px;
    ">
        <h3 style="color: #FF4B4B;">{titre}</h3>
        <p style="color: #31333F;">{contenu}</p>
    </div>
    """


col1, col2 = st.columns(2)

######## RECOMMANDATION ########
from item_to_reco import afficher_recommandations

@st.cache_data
def load_data():
    # Chemin absolu basé sur l'emplacement du script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    df_items = pd.read_csv(os.path.join(base_dir, "items.csv"))
    df_reco  = pd.read_csv(os.path.join(base_dir, "final_submission-2.csv"))
    
    return df_items, df_reco

df_items, df_reco = load_data()


col1, col2 = st.columns(2)

with col1:
    # On utilise le container pour créer le cadre global
    with st.container(border=True):
        # On injecte le style uniquement pour le titre ou le fond si tu veux
        st.markdown(
            """
            <div style="
                background-color: rgba(250, 249, 246, 0.85); 
                padding: 10px; 
                border-radius: 10px;
                margin-bottom: 10px;
            ">
                <h3 style='color: #FF4B4B; text-align: center; margin: 0;'>Get a recommendation</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.write("Find your next favorite book based on your ID.")
        
        # Les widgets Streamlit (ils doivent être HORS du st.markdown)
        user_id = st.number_input(
            "Enter User ID :", 
            min_value=0, 
            max_value=len(df_reco)-1, 
            step=1, 
            key="user_reco"
        )

        if st.button("My books recommandations"):
            afficher_recommandations(user_id, df_reco, df_items)

with col2:
    with st.container(border=True):
        st.markdown("<h3 style='color: #FF4B4B; text-align: center;'>Bloc Droite</h3>", unsafe_allow_html=True)
        st.write("Autres données ici")