import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from top_books import safe_str, safe_cover, generate_fallback_cover


def afficher_recommandations(user_id, df_reco, df_enriched):

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

    # --- Construire les données JS pour le modal ---
    books_js = "const BOOKS = [\n"
    cards_html = ""

    for rank, (_, book) in enumerate(df_books.iterrows(), start=1):
        title  = safe_str(book['Title'],  'Unknown Title')
        author = safe_str(book['Author'], 'Unknown Author')

        desc = safe_str(book.get('api_description', None), '')
        if not desc or desc == 'Unknown':
            desc = safe_str(book.get('description_x', None), '')
        if not desc or desc == 'Unknown':
            desc = "No description available for this book."

        cover = safe_cover(book)
        if not cover:
            cover = generate_fallback_cover(title, author)

        # Stocker les données complètes en JS pour le modal
        books_js += f"""  {{
    rank: {rank},
    title: "{esc(title)}",
    author: "{esc(author)}",
    desc: "{esc(desc)}",
    cover: "{cover if not cover.startswith('data:image/svg') else 'SVG'}"
  }},\n"""

        desc_short = desc[:160] + "…" if len(desc) > 160 else desc
        has_more = len(desc) > 160

        cards_html += f"""
        <div class="flip-container" id="card-{rank}" onclick="handleFlip(event, {rank})">
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
                    {"" if not has_more else f'<button class="read-more-btn" onclick="openModal(event, {rank})">Read more →</button>'}
                    <div class="back-hint">tap to flip back</div>
                </div>
            </div>
            <div class="card-label">{esc(title[:32] + ('…' if len(title) > 32 else ''))}</div>
        </div>
        """

    books_js += "];\n"

    nb_rows = -(-len(df_books) // 3)
    height  = 60 + nb_rows * 305

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
            margin-top: 6px;
        }}

        /* Bouton Read more */
        .read-more-btn {{
            background: rgba(255,255,255,0.15);
            border: 1px solid rgba(255,255,255,0.35);
            color: white;
            font-size: 0.6rem;
            padding: 4px 10px;
            border-radius: 20px;
            cursor: pointer;
            font-family: 'Lora', serif;
            margin-top: 6px;
            transition: background 0.2s;
            width: fit-content;
            align-self: flex-end;
        }}
        .read-more-btn:hover {{
            background: rgba(255,255,255,0.28);
        }}

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

        /* ====== MODAL OVERLAY ====== */
        .modal-overlay {{
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            z-index: 1000;
            align-items: flex-start;
            justify-content: center;
            padding-top: 40px;
            overflow-y: auto;
        }}
        .modal-overlay.active {{
            display: flex;
            animation: fadeIn 0.25s ease;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to   {{ opacity: 1; }}
        }}

        .modal-card {{
            background: linear-gradient(145deg, #1f6f43, #155230);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            width: 85%;
            max-width: 480px;
            max-height: 80vh;
            overflow-y: auto;
            display: flex;
            flex-direction: row;
            gap: 0;
            animation: scaleIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            position: relative;
        }}
        @keyframes scaleIn {{
            from {{ transform: scale(0.7); opacity: 0; }}
            to   {{ transform: scale(1);   opacity: 1; }}
        }}

        /* Image à gauche dans le modal */
        .modal-cover {{
            width: 140px;
            min-width: 140px;
            border-radius: 20px 0 0 20px;
            object-fit: cover;
        }}

        /* Contenu à droite */
        .modal-content {{
            padding: 20px 18px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex: 1;
        }}
        .modal-rank {{
            font-size: 0.7rem;
            color: rgba(255,255,255,0.45);
            font-family: 'Playfair Display', serif;
        }}
        .modal-title {{
            font-family: 'Playfair Display', serif;
            font-size: 1.05rem;
            font-weight: bold;
            color: white;
            line-height: 1.3;
        }}
        .modal-author {{
            font-size: 0.8rem;
            color: rgba(255,255,255,0.65);
            font-style: italic;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }}
        .modal-desc {{
            font-size: 0.82rem;
            color: rgba(255,255,255,0.9);
            line-height: 1.65;
            font-family: 'Lora', serif;
            flex: 1;
        }}
        .modal-close {{
            position: absolute;
            top: 12px;
            right: 14px;
            background: rgba(255,255,255,0.15);
            border: none;
            color: white;
            font-size: 1rem;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        }}
        .modal-close:hover {{
            background: rgba(255,255,255,0.3);
        }}
    </style>
    </head>
    <body>

        <div class="section-title">✨ Top 10 Recommendations for User {user_id}</div>
        <div class="flip-grid">
            {cards_html}
        </div>

        <!-- Modal overlay -->
        <div class="modal-overlay" id="modal" onclick="closeModalOutside(event)">
            <div class="modal-card" id="modal-card">
                <button class="modal-close" onclick="closeModal()">✕</button>
                <img class="modal-cover" id="modal-cover" src="" alt=""/>
                <div class="modal-content">
                    <div class="modal-rank"  id="modal-rank"></div>
                    <div class="modal-title" id="modal-title"></div>
                    <div class="modal-author" id="modal-author"></div>
                    <div class="modal-desc"  id="modal-desc"></div>
                </div>
            </div>
        </div>

        <script>
        {books_js}

        function handleFlip(event, rank) {{
            // Ne pas flipper si on clique sur Read more
            if (event.target.classList.contains('read-more-btn')) return;
            const card = document.getElementById('card-' + rank);
            card.classList.toggle('flipped');
        }}

        function openModal(event, rank) {{
            event.stopPropagation();
            const b = BOOKS[rank - 1];

            document.getElementById('modal-rank').textContent   = '#' + b.rank;
            document.getElementById('modal-title').textContent  = b.title;
            document.getElementById('modal-author').textContent = b.author;
            document.getElementById('modal-desc').textContent   = b.desc;

            const coverEl = document.getElementById('modal-cover');
            if (b.cover === 'SVG') {{
                coverEl.style.display = 'none';
            }} else {{
                coverEl.src = b.cover;
                coverEl.style.display = 'block';
            }}

            document.getElementById('modal').classList.add('active');
        }}

        function closeModal() {{
            document.getElementById('modal').classList.remove('active');
        }}

        function closeModalOutside(event) {{
            if (event.target === document.getElementById('modal')) closeModal();
        }}

        // Fermer avec Escape
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') closeModal();
        }});
        </script>
    </body>
    </html>
    """

    components.html(full_html, height=height, scrolling=True)