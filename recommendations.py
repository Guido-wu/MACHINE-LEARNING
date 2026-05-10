import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from top_books import safe_str, safe_cover, generate_fallback_cover


def afficher_recommandations(user_id, df_reco, df_enriched):

    # --- Trouver les recommandations ---
    row = df_reco[df_reco['user_id'] == user_id]
    if row.empty:
        st.error(f"❌ No recommendations found for User {user_id}.")
        return

    reco_ids = [int(x) for x in str(row['recommendation'].values[0]).split()][:10]

    df_books = df_enriched[df_enriched['i'].isin(reco_ids)].copy()
    df_books['reco_order'] = df_books['i'].apply(lambda x: reco_ids.index(x) if x in reco_ids else 99)
    df_books = df_books.sort_values('reco_order').reset_index(drop=True)

    def esc(s):
        return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'",'&#39;')

    # --- Construire les cartes ---
    cards_html = ""
    for rank, (_, book) in enumerate(df_books.iterrows(), start=1):
        title  = safe_str(book['Title'],  'Unknown Title')
        author = safe_str(book['Author'], 'Unknown Author')

        desc = safe_str(book.get('api_description', None), '')
        if not desc or desc == 'Unknown':
            desc = safe_str(book.get('description_x', None), '')
        if not desc or desc == 'Unknown':
            desc = "No description available for this book."
        desc_short = desc[:250] + "…" if len(desc) > 250 else desc

        cover = safe_cover(book)
        if not cover:
            cover = generate_fallback_cover(title, author)

        cards_html += f"""
        <div class="flip-container" onclick="this.classList.toggle('flipped')">
            <div class="flip-inner">

                <div class="flip-front">
                    <span class="flip-rank">#{rank}</span>
                    <img src="{cover}" alt="{esc(title)}"/>
                    <span class="flip-hint">tap to flip</span>
                </div>

                <div class="flip-back">
                    <div class="back-rank">#{rank}</div>
                    <div class="back-title">{esc(title)}</div>
                    <div class="back-author">{esc(author)}</div>
                    <div class="back-desc">{esc(desc_short)}</div>
                    <div class="back-hint">tap to flip back</div>
                </div>

            </div>
            <div class="card-label">{esc(title[:32] + ('…' if len(title) > 32 else ''))}</div>
        </div>
        """

    # --- HTML complet dans components.html (JS autorisé ici) ---
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8"/>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lora:ital@0;1&display=swap" rel="stylesheet"/>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: transparent;
            font-family: 'Lora', Georgia, serif;
            padding: 10px;
        }}

        .section-title {{
            font-family: 'Playfair Display', serif;
            color: #1f6f43;
            font-size: 1.15rem;
            font-weight: bold;
            margin-bottom: 20px;
            padding-bottom: 8px;
            border-bottom: 2px solid #1f6f43;
        }}

        /* Grille 3 colonnes */
        .flip-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 28px 20px;
        }}

        /* Flip container */
        .flip-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }}

        .flip-inner {{
            width: 160px;
            height: 230px;
            perspective: 1000px;
            position: relative;
        }}

        .flip-front, .flip-back {{
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 12px;
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;
            transition: transform 0.65s cubic-bezier(0.4, 0.2, 0.2, 1);
            overflow: hidden;
        }}

        /* Recto */
        .flip-front {{
            background: #e8dfc8;
            transform: rotateY(0deg);
            box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        }}
        .flip-front img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 12px;
            display: block;
        }}
        .flip-rank {{
            position: absolute;
            top: 8px;
            left: 8px;
            background: #1f6f43;
            color: white;
            font-size: 0.7rem;
            font-weight: bold;
            padding: 3px 9px;
            border-radius: 20px;
            font-family: 'Playfair Display', serif;
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
            z-index: 2;
        }}
        .flip-hint {{
            position: absolute;
            bottom: 8px;
            right: 8px;
            background: rgba(0,0,0,0.45);
            color: rgba(255,255,255,0.9);
            font-size: 0.55rem;
            padding: 2px 7px;
            border-radius: 10px;
        }}

        /* Verso */
        .flip-back {{
            background: linear-gradient(145deg, #1f6f43 0%, #155230 100%);
            transform: rotateY(180deg);
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
            display: flex;
            flex-direction: column;
            padding: 14px 12px 10px 12px;
        }}
        .back-rank {{
            font-family: 'Playfair Display', serif;
            font-size: 0.65rem;
            color: rgba(255,255,255,0.5);
            margin-bottom: 4px;
        }}
        .back-title {{
            font-family: 'Playfair Display', serif;
            font-size: 0.78rem;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 5px;
            line-height: 1.3;
        }}
        .back-author {{
            font-size: 0.65rem;
            color: rgba(255,255,255,0.65);
            font-style: italic;
            margin-bottom: 9px;
            padding-bottom: 7px;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }}
        .back-desc {{
            font-size: 0.62rem;
            color: rgba(255,255,255,0.85);
            line-height: 1.55;
            flex: 1;
            overflow: hidden;
        }}
        .back-hint {{
            font-size: 0.5rem;
            color: rgba(255,255,255,0.35);
            text-align: center;
            margin-top: 8px;
        }}

        /* Label sous la carte */
        .card-label {{
            font-size: 0.68rem;
            color: #444;
            text-align: center;
            font-style: italic;
            max-width: 160px;
            line-height: 1.3;
        }}

        /* Flip actif */
        .flip-container.flipped .flip-front {{
            transform: rotateY(-180deg);
        }}
        .flip-container.flipped .flip-back {{
            transform: rotateY(0deg);
        }}
    </style>
    </head>
    <body>
        <div class="section-title">✨ Top 10 Recommendations for User {user_id}</div>
        <div class="flip-grid">
            {cards_html}
        </div>
    </body>
    </html>
    """

    # Hauteur dynamique selon nb de lignes (3 par ligne)
    nb_rows = -(-len(df_books) // 3)  # arrondi supérieur
    height  = 120 + nb_rows * 310

    components.html(full_html, height=height, scrolling=False)