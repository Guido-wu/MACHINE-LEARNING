import streamlit as st
import pandas as pd




# Chargement des données
@st.cache_data



def afficher_recommandations(df_reco, df_items):
    # L'input pour l'ID utilisateur
    user_id = st.number_input("Entrez votre User ID :", min_value=0, max_value=len(df_reco)-1, step=1)

    if st.button("Afficher mes 10 recommandations"):
        # Récupération de la ligne correspondant à l'ID
        row = df_reco[df_reco['user_id'] == user_id]
        
        if not row.empty:
            # Extraction et conversion des IDs de recommandations
            reco_ids = [int(i) for i in row['recommendation'].values[0].split()]
            
            st.subheader(f" Top 10 books that fits you {user_id}")
            
            # Création d'un conteneur pour un affichage plus propre
            with st.container():
                for i, book_id in enumerate(reco_ids):
                    # Recherche dans le catalogue items.csv
                    book_info = df_items[df_items['i'] == book_id]
                    
                    if not book_info.empty:
                        title = book_info['title'].values[0]
                        # Gestion de l'auteur (vérifie si la colonne s'appelle 'Author' ou 'author' dans ton CSV)
                        author = book_info.get('author', book_info.get('Author', 'Auteur inconnu')).values[0]
                        
                        st.write(f"**{i+1}. {title}**")
                        st.caption(f"{author}")
                        st.write("---") # Petite ligne de séparation
        else:
            st.error("❌ User not found.")