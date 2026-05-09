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