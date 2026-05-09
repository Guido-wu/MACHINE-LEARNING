import streamlit as st  # <--- IL MANQUE CETTE LIGNE
import base64
import os

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()



def afficher_image_fond(nom_fichier):
    import base64
    import os
    if os.path.exists(nom_fichier):
        with open(nom_fichier, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
                .background-logo {{
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    width: 250px;
                    opacity: 0.08;
                    z-index: -1;
                    pointer-events: none;
                }}
            </style>
            <img src="data:image/png;base64,{encoded}" class="background-logo">
            """,
            unsafe_allow_html=True
        )