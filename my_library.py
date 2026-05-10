import streamlit as st
import pandas as pd
from top_books import safe_str, safe_cover, generate_fallback_cover

# Emojis par catégorie
CATEGORY_ICONS = {
    "Literature & Fiction": "📖",
    "Comics & Graphic Novels": "💬",
    "History": "🏛️",
    "Education & Pedagogy": "🎓",
    "Social Sciences & Sociology": "🌍",
    "Children's Literature": "🧒",
    "Law & Justice": "⚖️",
    "Psychology & Mental Health": "🧠",
    "Arts & Art History": "🎨",
    "Political Science": "🗳️",
    "Swiss Studies": "🇨🇭",
    "Geography & Travel": "✈️",
    "Medicine & Health": "🏥",
    "Economics & Management": "📈",
    "Linguistics & Languages": "🗣️",
    "Philosophy & Ethics": "💭",
    "Environment & Ecology": "🌿",
    "Gastronomy & Food": "🍽️",
    "Religion & Spirituality": "✨",
    "Science & Technology": "🔬",
    "Music": "🎵",
    "Cinema & Theater": "🎬",
    "Sports & Leisure": "⚽",
    "Uncategorized": "📚",
    "Other": "📚",
}

def get_icon(cat):
    return CATEGORY_ICONS.get(cat, "📚")


def afficher_my_library(user_id, df_interactions, df_categories, df_enriched):
    """
    Affiche les livres lus par un utilisateur, groupés par catégorie avec covers.
    df_categories : items_with_categories.csv
    df_enriched   : items_enriched_api.csv (pour les covers)
    """

    # CSS
    st.markdown("""
    <style>
    .lib-category-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        color: #1f6f43;
        font-weight: bold;
        margin: 24px 0 10px 0;
        padding-bottom: 6px;
        border-bottom: 2px solid #1f6f43;
    }
    .lib-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        margin-bottom: 10px;
    }
    .lib-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
        width: 100px;
        cursor: default;
    }
    .lib-cover {
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        object-fit: cover;
        transition: transform .2s, box-shadow .2s;
    }
    .lib-cover:hover {
        transform: scale(1.07);
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }
    .lib-title {
        font-size: 0.65rem;
        color: #333;
        text-align: center;
        font-style: italic;
        line-height: 1.3;
        max-width: 100px;
    }
    .lib-author {
        font-size: 0.6rem;
        color: #1f6f43;
        text-align: center;
        max-width: 100px;
    }
    .lib-empty {
        color: #aaa;
        font-style: italic;
        font-size: 0.9rem;
        padding: 20px 0;
    }
    .lib-stats {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 14px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        display: flex;
        gap: 30px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    .lib-stat-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .lib-stat-number {
        font-size: 1.6rem;
        font-weight: bold;
        color: #1f6f43;
        font-family: 'Playfair Display', serif;
    }
    .lib-stat-label {
        font-size: 0.7rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    </style>
    """, unsafe_allow_html=True)

    # Livres lus par cet utilisateur
    user_items = df_interactions[df_interactions['u'] == user_id]['i'].tolist()

    if not user_items:
        st.markdown('<p class="lib-empty">No reading history found for this user.</p>', unsafe_allow_html=True)
        return

    # Joindre avec catégories et enriched (pour la cover)
    df_user = df_categories[df_categories['i'].isin(user_items)].copy()
    df_user = df_user.merge(
        df_enriched[['i', 'api_thumbnail']],
        on='i', how='left'
    )

    nb_books = len(df_user)
    nb_cats  = df_user['Catégorie'].nunique()

    # Stats bar
    st.markdown(f"""
    <div class="lib-stats">
        <div class="lib-stat-item">
            <span class="lib-stat-number">{nb_books}</span>
            <span class="lib-stat-label">Books read</span>
        </div>
        <div class="lib-stat-item">
            <span class="lib-stat-number">{nb_cats}</span>
            <span class="lib-stat-label">Categories</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Grouper par catégorie, trier par nb de livres décroissant
    cats_sorted = df_user['Catégorie'].value_counts().index.tolist()

    # Filtrer les catégories peu intéressantes en dernier
    priority = [c for c in cats_sorted if c not in ('Uncategorized', 'Other')]
    rest     = [c for c in cats_sorted if c in ('Uncategorized', 'Other')]
    cats_sorted = priority + rest

    for cat in cats_sorted:
        books_in_cat = df_user[df_user['Catégorie'] == cat]
        icon = get_icon(cat)
        nb   = len(books_in_cat)

        st.markdown(
            f'<div class="lib-category-header">{icon} {cat} <span style="color:#aaa;font-size:0.85rem;font-weight:normal;">({nb} book{"s" if nb > 1 else ""})</span></div>',
            unsafe_allow_html=True
        )

        html = '<div class="lib-grid">'
        for _, row in books_in_cat.iterrows():
            cover = safe_cover(row)
            if not cover:
                cover = generate_fallback_cover(row['Title'], row['Author'])

            title  = safe_str(row['Title'])[:26] + "…" if len(safe_str(row['Title'])) > 26 else safe_str(row['Title'])
            author = safe_str(row['Author'])[:22] + "…" if len(safe_str(row['Author'])) > 22 else safe_str(row['Author'])

            html += f"""
            <div class="lib-card">
                <img src="{cover}" width="90" height="130" class="lib-cover"/>
                <span class="lib-title">{title}</span>
                <span class="lib-author">{author}</span>
            </div>"""

        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)