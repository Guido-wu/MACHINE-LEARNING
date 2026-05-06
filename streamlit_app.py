import streamlit as st



#Ajout d'un titre et d'un sous titre dans l'application 
st.set_page_config(
    page_title="Omega Book Recommendation",
    page_icon="📚",
    layout="wide"
)

# Style pour le titre et le sous-titre

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Trebuchet MS", sans-serif; color: white;'>
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

