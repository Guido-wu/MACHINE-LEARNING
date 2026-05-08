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

with col1:
    st.markdown(bloc_style(
        "New user - Get a recommandation", 
        "Click here to get a personalized book recommendation based on your preferences!"
        ), 
        unsafe_allow_html=True)

with col2:
    st.markdown(bloc_style("Bloc Droite", "Autres données ici"), unsafe_allow_html=True)


with st.expander("👉 Cliquez ici pour ouvrir le moteur de recherche"):
    st.write("Ici, on mettra les filtres de livres (Genre, Auteur, etc.)")
    choix = st.selectbox("Quel style aimes-tu ?", ["Thriller", "Roman", "SF"])







######## RECOMMANDATION ########
from item_to_reco import afficher_recommandations
st.write(os.listdir(os.path.dirname(os.path.abspath(__file__))))
@st.cache_data
def load_data():
    # Chemin absolu basé sur l'emplacement du script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    df_items = pd.read_csv(os.path.join(base_dir, "items.csv"))
    df_reco  = pd.read_csv(os.path.join(base_dir, "final_submission-2.csv"))
    
    return df_items, df_reco

df_items, df_reco = load_data()


# L'input pour l'ID utilisateur
user_id = st.number_input("Entrez votre User ID :", min_value=0, max_value=len(df_reco)-1, step=1)


if st.button("My books recommandations"):
    # On appelle la fonction qui vient de l'autre fichier
    Books = afficher_recommandations(user_id, df_reco, df_items)
'''
    if Books is not None:
        for index, row in Books.iterrows():
            st.write(f"📖 **{row['title']}**")
    else:
        st.error("Utilisateur inconnu")
'''