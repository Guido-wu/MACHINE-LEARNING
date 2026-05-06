import streamlit as st
import base64



#Ajout d'un titre et d'un sous titre dans l'application 
st.set_page_config(
    page_title="Omega Book Recommendation",
    page_icon="📚",
    layout="wide"
)

# Style pour le titre et le sous-titre

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Trebuchet MS", sans-serif; color: black;'>
        Welcome to our books recomendation app !!
    </h1>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align: center; font-family: "Courier New", monospace; font-size: 20px;'>
    Find the book that fits you the best !
    </p>
    """, 
    unsafe_allow_html=True
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
        url("data:image/jpeg;base64,{img_base64}");
        background-attachment: fixed;
        background-size: cover;
        backdrop-filter: blur(5px); /* Ajoute un léger flou */
    }

    </style>
    """,
    unsafe_allow_html=True
)


