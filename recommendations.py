import streamlit as st
import pandas as pd
from top_books import safe_str, safe_cover, generate_fallback_cover


def afficher_recommandations(user_id, df_reco, df_enriched):
    """
    Affiche le Top 10 des recommandations pour un user,
    avec flip card : recto = cover, verso = description.
    """

    # --- Trouver les recommandations de l'utilisateur ---
    row = df_reco[df_reco['user_id'] == user_id]
    if row.empty:
        st.error(f"❌ No recommendations found for User {user_id}.")
        return

    reco_ids = [int(x) for x in str(row['recommendation'].values[0]).split()][:10]

    # --- Joindre avec les infos enrichies ---
    df_books = df_enriched[df_enriched['i'].isin(reco_ids)].copy()

    # Réordonner selon l'ordre des recommandations
    df_books['reco_order'] = df_books['i'].apply(lambda x: reco_ids.index(x) if x in reco_ids else 99)
    df_books = df_books.sort_values('reco_order').reset_index(drop=True)

    # --- CSS flip cards ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lora:ital@0;1&display=swap');

    .reco-header {
        font-family: 'Playfair Display', serif;
        color: #1f6f43;
        font-size: 1.1rem;
        margin-bottom: 18px;
        padding-bottom: 8px;
        border-bottom: 2px solid #1f6f43;
    }

    .flip-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: flex-start;
        margin-top: 10px;
    }

    .flip-container {
        width: 130px;
        height: 195px;
        perspective: 900px;
        cursor: pointer;
    }

    .flip-inner {
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
        border-radius: 10px;
    }

    .flip-container.flipped .flip-inner {
        transform: rotateY(180deg);
    }

    .flip-front, .flip-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        border-radius: 10px;
        overflow: hidden;
    }

    .flip-front {
        background: #f0e8d0;
    }

    .flip-front img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 10px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        display: block;
    }

    .flip-rank {
        position: absolute;
        top: 6px;
        left: 6px;
        background-color: #1f6f43;
        color: white;
        font-size: 0.65rem;
        font-weight: bold;
        padding: 2px 7px;
        border-radius: 20px;
        font-family: 'Playfair Display', serif;
        z-index: 2;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }

    .flip-back {
        background: linear-gradient(145deg, #1f6f43, #155230);
        transform: rotateY(180deg);
        display: flex;
        flex-direction: column;
        padding: 10px 8px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        box-sizing: border-box;
    }

    .flip-back-title {
        font-family: 'Playfair Display', serif;
        font-size: 0.68rem;
        font-weight: bold;
        color: #fff;
        margin-bottom: 4px;
        line-height: 1.3;
    }

    .flip-back-author {
        font-size: 0.58rem;
        color: rgba(255,255,255,0.7);
        font-style: italic;
        margin-bottom: 7px;
        padding-bottom: 5px;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }

    .flip-back-desc {
        font-size: 0.58rem;
        color: rgba(255,255,255,0.88);
        line-height: 1.5;
        overflow: hidden;
        flex: 1;
        font-family: 'Lora', serif;
    }

    .flip-back-hint {
        font-size: 0.52rem;
        color: rgba(255,255,255,0.4);
        text-align: center;
        margin-top: 5px;
    }

    .flip-front-hint {
        position: absolute;
        bottom: 6px;
        right: 6px;
        font-size: 0.55rem;
        color: rgba(255,255,255,0.8);
        background: rgba(0,0,0,0.4);
        padding: 2px 5px;
        border-radius: 8px;
        z-index: 2;
    }

    .reco-card-label {
        font-size: 0.65rem;
        color: #555;
        text-align: center;
        font-style: italic;
        max-width: 130px;
        margin-top: 5px;
        line-height: 1.3;
    }
    </style>

    <script>
    function flipCard(el) {
        el.classList.toggle('flipped');
    }
    </script>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="reco-header">✨ Top 10 Recommendations for User {user_id}</div>', unsafe_allow_html=True)

    st.markdown('<div class="flip-grid">', unsafe_allow_html=True)

    for rank, (_, book) in enumerate(df_books.iterrows(), start=1):
        title  = safe_str(book['Title'], 'Unknown Title')
        author = safe_str(book['Author'], 'Unknown Author')

        desc = safe_str(book.get('api_description', None), '')
        if not desc or desc == 'Unknown':
            desc = safe_str(book.get('description_x', None), '')
        if not desc or desc == 'Unknown':
            desc = "No description available for this book."

        desc_short = desc[:200] + "…" if len(desc) > 200 else desc

        def esc(s):
            return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'",'&#39;')

        title_esc   = esc(title)
        author_esc  = esc(author)
        desc_esc    = esc(desc_short)
        title_short = title[:28] + "…" if len(title) > 28 else title

        cover = safe_cover(book)
        if not cover:
            cover = generate_fallback_cover(title, author)

        # Une carte à la fois → pas de limite de taille
        st.markdown(f"""
        <div style="display:inline-flex;flex-direction:column;align-items:center;margin:10px;">
            <div class="flip-container" onclick="flipCard(this)">
                <div class="flip-inner">
                    <div class="flip-front">
                        <span class="flip-rank">#{rank}</span>
                        <img src="{cover}" alt="{title_esc}"/>
                        <span class="flip-front-hint">tap ↩</span>
                    </div>
                    <div class="flip-back">
                        <div class="flip-back-title">{title_esc}</div>
                        <div class="flip-back-author">{author_esc}</div>
                        <div class="flip-back-desc">{desc_esc}</div>
                        <div class="flip-back-hint">tap to flip back</div>
                    </div>
                </div>
            </div>
            <div class="reco-card-label">{esc(title_short)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)