import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# ---------------------------------------------------------
# FALLBACK COVER : carte SVG stylée si pas de thumbnail
# ---------------------------------------------------------
def generate_fallback_cover(title, author, rank=None):
    short_title = title[:35] + "..." if len(title) > 35 else title
    short_author = author[:25] + "..." if len(author) > 25 else author

    medal = ""
    bg_color = "#1f6f43"
    if rank == 1:
        medal = "🥇"
        bg_color = "#b8860b"
    elif rank == 2:
        medal = "🥈"
        bg_color = "#708090"
    elif rank == 3:
        medal = "🥉"
        bg_color = "#8B4513"

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="140" height="200" viewBox="0 0 140 200">
      <rect width="140" height="200" rx="8" fill="{bg_color}"/>
      <rect x="8" y="8" width="124" height="184" rx="6" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
      <text x="70" y="45" font-family="Georgia,serif" font-size="28" fill="rgba(255,255,255,0.2)" text-anchor="middle">📖</text>
      <text x="70" y="42" font-family="Georgia,serif" font-size="22" fill="white" text-anchor="middle">{medal}</text>
      <foreignObject x="10" y="55" width="120" height="100">
        <div xmlns="http://www.w3.org/1999/xhtml" style="
          font-family: Georgia, serif;
          font-size: 11px;
          font-weight: bold;
          color: white;
          text-align: center;
          word-wrap: break-word;
          line-height: 1.4;
        ">{short_title}</div>
      </foreignObject>
      <line x1="20" y1="162" x2="120" y2="162" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
      <foreignObject x="10" y="166" width="120" height="26">
        <div xmlns="http://www.w3.org/1999/xhtml" style="
          font-family: Georgia, serif;
          font-size: 9px;
          font-style: italic;
          color: rgba(255,255,255,0.8);
          text-align: center;
          word-wrap: break-word;
        ">{short_author}</div>
      </foreignObject>
    </svg>
    """
    b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{b64}"


# ---------------------------------------------------------
# TOP 3 BOOKS — PODIUM
# ---------------------------------------------------------
def afficher_top_books(df_enriched, df_interactions):
    # Compter les interactions par livre
    top_ids = df_interactions['i'].value_counts().head(3).reset_index()
    top_ids.columns = ['i', 'count']

    # Joindre avec les infos enrichies
    top_books = top_ids.merge(df_enriched[['i', 'Title', 'Author', 'api_thumbnail']], on='i', how='left')

    # Ordre podium : 2e, 1er, 3e (visuellement)
    podium_order = [1, 0, 2]  # indices dans top_books
    podium_heights = ["160px", "210px", "130px"]
    podium_colors = ["#9e9e9e", "#b8860b", "#8B4513"]
    podium_labels = ["🥈 2nd", "🥇 1st", "🥉 3rd"]
    podium_ranks = [2, 1, 3]

    st.markdown("""
        <style>
        .podium-wrapper {
            display: flex;
            justify-content: center;
            align-items: flex-end;
            gap: 20px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .podium-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }
        .podium-cover {
            border-radius: 10px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            transition: transform 0.2s ease;
            object-fit: cover;
        }
        .podium-cover:hover {
            transform: scale(1.05);
        }
        .podium-base {
            border-radius: 10px 10px 0 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: white;
            font-family: 'Playfair Display', serif;
            font-size: 0.85rem;
            width: 120px;
        }
        .podium-title {
            font-size: 0.72rem;
            color: #444;
            text-align: center;
            max-width: 130px;
            line-height: 1.3;
            font-style: italic;
        }
        .podium-count {
            font-size: 0.68rem;
            color: #1f6f43;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    html = '<div class="podium-wrapper">'

    for pos, idx in enumerate(podium_order):
        if idx >= len(top_books):
            continue
        row = top_books.iloc[idx]
        rank = podium_ranks[pos]
        height = podium_heights[pos]
        color = podium_colors[pos]
        label = podium_labels[pos]

        # Cover
        cover_url = row.get('api_thumbnail', None)
        if pd.isna(cover_url) or not cover_url:
            cover_url = generate_fallback_cover(row['Title'], row['Author'], rank)
            img_w, img_h = 110, 155
        else:
            img_w, img_h = 110, 155

        short_title = row['Title'][:30] + "..." if len(str(row['Title'])) > 30 else row['Title']

        html += f"""
        <div class="podium-item">
            <img src="{cover_url}" width="{img_w}" height="{img_h}" class="podium-cover"/>
            <span class="podium-title">{short_title}</span>
            <span class="podium-count">📖 {int(row['count'])} reads</span>
            <div class="podium-base" style="background-color:{color}; height:{height};">
                {label}
            </div>
        </div>
        """

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------
# NEW RELEASES
# ---------------------------------------------------------
def afficher_new_releases(df_enriched):
    # Extraire l'année et filtrer les plus récents avec cover
    df = df_enriched.copy()
    df['year'] = pd.to_numeric(df['api_published_date'].str[:4], errors='coerce')
    df_recent = df[df['year'] >= 2022].sort_values('year', ascending=False)

    # Prendre les 6 premiers (avec ou sans cover)
    top_recent = df_recent.head(20).drop_duplicates(subset='Title').head(6)

    st.markdown("""
        <style>
        .releases-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            justify-content: flex-start;
            margin-top: 10px;
        }
        .release-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            width: 110px;
        }
        .release-cover {
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            object-fit: cover;
            transition: transform 0.2s ease;
        }
        .release-cover:hover { transform: scale(1.05); }
        .release-title {
            font-size: 0.7rem;
            color: #333;
            text-align: center;
            font-style: italic;
            line-height: 1.3;
        }
        .release-year {
            font-size: 0.65rem;
            color: #1f6f43;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    html = '<div class="releases-grid">'
    for _, row in top_recent.iterrows():
        cover_url = row.get('api_thumbnail', None)
        if pd.isna(cover_url) or not cover_url:
            cover_url = generate_fallback_cover(row['Title'], row.get('Author', ''))

        short_title = row['Title'][:28] + "..." if len(str(row['Title'])) > 28 else row['Title']
        year = int(row['year']) if not pd.isna(row['year']) else "?"

        html += f"""
        <div class="release-card">
            <img src="{cover_url}" width="100" height="145" class="release-cover"/>
            <span class="release-title">{short_title}</span>
            <span class="release-year">✨ {year}</span>
        </div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)