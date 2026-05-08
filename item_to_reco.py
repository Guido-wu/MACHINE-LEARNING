import streamlit as st
import pandas as pd





def afficher_recommandations(user_id, df_reco, df_items):
    row = df_reco[df_reco['user_id'] == user_id]
    
    if not row.empty:
        reco_ids = [int(i) for i in row['recommendation'].values[0].split()]
        st.subheader(f"✨ Top 10 books that fit you (User {user_id})")
        
        with st.container():
            for i, book_id in enumerate(reco_ids):
                book_info = df_items[df_items['i'] == book_id]
                if not book_info.empty:
                    title = book_info['Title'].values[0]
                    author = book_info.get('Author', book_info.get('Author', 'Unknown Author')).values[0]
                    st.write(f"**{i+1}. {title}**")
                    st.caption(f"✍️ {author}")
                    st.write("---")
    else:
        st.error("❌ User not found.")