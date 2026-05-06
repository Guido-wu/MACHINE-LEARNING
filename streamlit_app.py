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


