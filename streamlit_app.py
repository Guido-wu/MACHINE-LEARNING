import streamlit as st
import base64



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
        url("https://images.unsplash.com/photo-1507842217343-583bb7270b66?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80");
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
for _ in range(15):
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

col1, col2 = st.columns(2)

with col1:
    st.header("Colonne de gauche")
    st.write("Tu peux mettre des graphiques, du texte ou des widgets ici.")
    st.button("Bouton de gauche")

with col2:
    st.header("Colonne de droite")
    st.write("Ici, on peut mettre une image ou d'autres données.")
    st.checkbox("Coche-moi")



with st.expander("👉 Cliquez ici pour ouvrir le moteur de recherche"):
    st.write("Ici, on mettra les filtres de livres (Genre, Auteur, etc.)")
    choix = st.selectbox("Quel style aimes-tu ?", ["Thriller", "Roman", "SF"])