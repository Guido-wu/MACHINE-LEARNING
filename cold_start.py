import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from top_books import safe_str, safe_cover, generate_fallback_cover

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
}


# ------------------------------------------------------------------
# ÉTAPE 1 : Sélection des catégories
# ------------------------------------------------------------------
def step_categories(df_categories):
    st.markdown("""
        <div style="text-align:center; margin-bottom: 24px;">
            <h2 style="font-family:'Playfair Display',serif; color:#1f6f43;">
                What kind of books do you enjoy? 📚
            </h2>
            <p style="color:#666; font-size:0.95rem;">
                Choose <strong>3 categories</strong> that interest you most
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Catégories disponibles (sans Uncategorized / Other)
    all_cats = df_categories['Catégorie'].value_counts()
    all_cats = all_cats[~all_cats.index.isin(['Uncategorized', 'Other'])].index.tolist()

    selected = st.session_state.get('cold_start_cats', [])

    # CSS pour les boutons catégorie
    st.markdown("""
    <style>
    div[data-testid="column"] button {
        width: 100% !important;
        border-radius: 12px !important;
        padding: 12px 8px !important;
        font-size: 0.85rem !important;
        transition: all 0.2s !important;
        border: 2px solid #1f6f43 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Grille 4 colonnes
    cols = st.columns(4)
    for i, cat in enumerate(all_cats):
        icon = CATEGORY_ICONS.get(cat, "📚")
        is_selected = cat in selected
        label = f"{'✅ ' if is_selected else ''}{icon} {cat}"

        with cols[i % 4]:
            if st.button(label, key=f"cat_{cat}"):
                if cat in selected:
                    selected.remove(cat)
                else:
                    if len(selected) < 3:
                        selected.append(cat)
                    else:
                        st.warning("You can only select 3 categories. Deselect one first.")
                st.session_state['cold_start_cats'] = selected
                st.rerun()

    st.markdown(f"""
        <div style="text-align:center; margin-top:20px; color:#1f6f43; font-weight:bold;">
            {len(selected)}/3 categories selected : {' • '.join([CATEGORY_ICONS.get(c,'📚')+' '+c for c in selected])}
        </div>
    """, unsafe_allow_html=True)

    if len(selected) == 3:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next → Choose books you'd like to read", use_container_width=True):
                st.session_state['cold_start_step'] = 2
                st.rerun()


# ------------------------------------------------------------------
# ÉTAPE 2 : Sélection des livres (100% Streamlit natif)
# ------------------------------------------------------------------
def step_books(df_categories, df_interactions, df_enriched):
    selected_cats = st.session_state.get('cold_start_cats', [])

    st.markdown(f"""
        <div style="text-align:center; margin-bottom:20px;">
            <h2 style="font-family:'Playfair Display',serif; color:#1f6f43;">
                Which books appeal to you? 👀
            </h2>
            <p style="color:#666; font-size:0.95rem;">
                Click the books you'd like to read — select at least <strong>3</strong>
                <br><small style="color:#aaa;">Based on: 
                {' • '.join([CATEGORY_ICONS.get(c,'📚')+' '+c for c in selected_cats])}</small>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # CSS pour cacher le label checkbox et styler le bouton
    st.markdown("""
    <style>
    /* Cache le label texte des checkboxes */
    div[data-testid="stCheckbox"] label p { display: none !important; }
    div[data-testid="stCheckbox"] { margin: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

    # Trouver les 20 livres les plus populaires dans les catégories choisies
    df_filtered = df_categories[df_categories['Catégorie'].isin(selected_cats)].copy()
    pop = df_interactions['i'].value_counts().reset_index()
    pop.columns = ['i', 'count']
    df_pop = df_filtered.merge(pop, on='i', how='left').sort_values('count', ascending=False)
    df_pop = df_pop.merge(df_enriched[['i', 'api_thumbnail']], on='i', how='left')

    candidates = []
    for cat in selected_cats:
        top_cat = df_pop[df_pop['Catégorie'] == cat].head(8)
        candidates.append(top_cat)
    df_20 = pd.concat(candidates).drop_duplicates(subset='i').head(20).reset_index(drop=True)

    # Initialiser la sélection dans session_state
    if 'cold_start_books' not in st.session_state:
        st.session_state['cold_start_books'] = []

    # Afficher en grille de 5 colonnes
    N_COLS = 5
    rows = [df_20.iloc[i:i+N_COLS] for i in range(0, len(df_20), N_COLS)]

    for row_df in rows:
        cols = st.columns(N_COLS)
        for col, (_, book) in zip(cols, row_df.iterrows()):
            item_id = int(book['i'])
            title   = safe_str(book['Title'], 'Unknown')
            author  = safe_str(book['Author'], 'Unknown')
            cat     = safe_str(book['Catégorie'], '')
            icon    = CATEGORY_ICONS.get(cat, "📚")
            is_sel  = item_id in st.session_state['cold_start_books']

            cover = safe_cover(book)
            if not cover:
                cover = generate_fallback_cover(title, author)

            with col:
                # Bordure verte si sélectionné
                border_color = "#1f6f43" if is_sel else "transparent"
                overlay_html = """
                    <div style="position:absolute;top:0;left:0;width:100%;height:100%;
                                background:rgba(31,111,67,0.5);border-radius:10px;
                                display:flex;align-items:center;justify-content:center;
                                font-size:2rem;color:white;font-weight:bold;">✓</div>
                """ if is_sel else ""

                st.markdown(f"""
                    <div style="display:flex;flex-direction:column;align-items:center;gap:5px;margin-bottom:4px;">
                        <div style="position:relative;border:3px solid {border_color};
                                    border-radius:10px;overflow:hidden;width:fit-content;">
                            <img src="{cover}" width="110" height="155"
                                 style="display:block;object-fit:cover;border-radius:8px;"/>
                            {overlay_html}
                        </div>
                        <span style="font-size:0.6rem;color:#1f6f43;font-weight:bold;text-align:center;">
                            {icon} {cat}
                        </span>
                        <span style="font-size:0.62rem;color:#333;font-style:italic;
                                     text-align:center;line-height:1.3;">
                            {title[:26]}{'…' if len(title)>26 else ''}
                        </span>
                    </div>
                """, unsafe_allow_html=True)

                # Checkbox native Streamlit (le seul élément interactif)
                checked = st.checkbox(
                    "select",
                    value=is_sel,
                    key=f"pick_{item_id}",
                    label_visibility="collapsed"
                )
                # Mettre à jour la sélection
                if checked and item_id not in st.session_state['cold_start_books']:
                    st.session_state['cold_start_books'].append(item_id)
                    st.rerun()
                elif not checked and item_id in st.session_state['cold_start_books']:
                    st.session_state['cold_start_books'].remove(item_id)
                    st.rerun()

    nb = len(st.session_state['cold_start_books'])

    # Compteur
    st.markdown(f"""
        <div style="text-align:center;margin:16px 0;font-family:'Playfair Display',serif;
                    color:#1f6f43;font-size:1rem;font-weight:bold;">
            {'✅' if nb >= 3 else '📚'} {nb} book{'s' if nb != 1 else ''} selected
            {' — ready to go!' if nb >= 3 else f' — select {3-nb} more'}
        </div>
    """, unsafe_allow_html=True)

    # Boutons navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back"):
            st.session_state['cold_start_step'] = 1
            st.session_state['cold_start_books'] = []
            st.rerun()
    with col3:
        if nb >= 3:
            if st.button("✨ Get my recommendations →", use_container_width=True):
                st.session_state['cold_start_step'] = 3
                st.rerun()

# ---- DEAD CODE BELOW (ancienne version JS) — à ignorer ----
def _dead_code():
    full_html = f"""
    <!DOCTYPE html><html><head><meta charset="utf-8"/>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lora&display=swap" rel="stylesheet"/>
    <style>
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    body {{ background:transparent; font-family:'Lora',serif; padding:8px; }}
    .pick-grid {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 16px;
    }}
    .book-pick {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
        cursor: pointer;
    }}
    .pick-img-wrap {{ transition: border 0.15s; }}
    .pick-img-wrap img {{ display:block; border-radius:8px; object-fit:cover; }}
    .pick-overlay {{
        position: absolute;
        top:0; left:0; width:100%; height:100%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.2s;
        border-radius: 8px;
    }}
    .pick-check {{
        font-size: 2rem;
        color: white;
        font-weight: bold;
    }}
    .book-pick:hover .pick-img-wrap {{
        transform: scale(1.04);
        transition: transform 0.15s;
    }}
    .pick-cat {{
        font-size: 0.58rem;
        color: #1f6f43;
        font-weight: bold;
        text-align: center;
    }}
    .pick-title {{
        font-size: 0.62rem;
        color: #333;
        text-align: center;
        font-style: italic;
        line-height: 1.3;
    }}
    #counter {{
        text-align: center;
        font-family: 'Playfair Display', serif;
        color: #1f6f43;
        font-size: 0.9rem;
        margin-bottom: 14px;
        font-weight: bold;
    }}
    </style>
    </head>
    <body>
    <div id="counter">{nb_selected} book{'s' if nb_selected != 1 else ''} selected</div>
    <div class="pick-grid">{cards_html}</div>

    <script>
    const selected = new Set({list(selected_books)});

    function toggleBook(id, el) {{
        const wrap = el.querySelector('.pick-img-wrap');
        const overlay = el.querySelector('.pick-overlay');
        const check = el.querySelector('.pick-check');

        if (selected.has(id)) {{
            selected.delete(id);
            wrap.style.border = '3px solid transparent';
            overlay.style.background = 'transparent';
            check.textContent = '';
        }} else {{
            selected.add(id);
            wrap.style.border = '3px solid #1f6f43';
            overlay.style.background = 'rgba(31,111,67,0.55)';
            check.textContent = '✓';
        }}

        document.getElementById('counter').textContent =
            selected.size + ' book' + (selected.size !== 1 ? 's' : '') + ' selected';

        // Envoyer la sélection à Streamlit via URL hash
        window.location.hash = 'books:' + Array.from(selected).join(',');
    }}
    </script>
    </body></html>
    """

    components.html(full_html, height=520, scrolling=False)

    # Récupérer la sélection via un text_input caché
    st.markdown("**Paste your selection code** (auto-filled after clicking books) :")
    raw = st.text_input(
        "Selected book IDs (comma-separated) :",
        value=','.join(map(str, selected_books)),
        key="cold_book_input",
        placeholder="e.g. 123,456,789"
    )

    # Parser la sélection
    try:
        parsed = [int(x.strip()) for x in raw.split(',') if x.strip().isdigit()]
    except:
        parsed = []
    st.session_state['cold_start_books'] = parsed

    nb = len(parsed)
    if nb > 0:
        st.markdown(f"<p style='color:#1f6f43; font-size:0.85rem;'>✅ {nb} book(s) selected</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back"):
            st.session_state['cold_start_step'] = 1
            st.rerun()
    with col3:
        if nb >= 3:
            if st.button("✨ Get my recommendations →", use_container_width=True):
                st.session_state['cold_start_step'] = 3
                st.rerun()
        else:
            st.markdown(f"<p style='color:#aaa; font-size:0.8rem;'>Select at least 3 books to continue ({nb}/3)</p>", unsafe_allow_html=True)


# ------------------------------------------------------------------
# ÉTAPE 3 : Similarité + recommandations
# ------------------------------------------------------------------
def step_recommendations(df_interactions, df_reco, df_enriched):
    selected_books = st.session_state.get('cold_start_books', [])
    selected_cats  = st.session_state.get('cold_start_cats', [])

    st.markdown("""
        <div style="text-align:center; margin-bottom:16px;">
            <h2 style="font-family:'Playfair Display',serif; color:#1f6f43;">
                Finding your perfect reads… 🔍
            </h2>
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Analyzing your taste profile..."):
        # Similarité de Jaccard entre le nouveau user et tous les users existants
        selected_set = set(selected_books)

        # Grouper les items par user
        user_items = df_interactions.groupby('u')['i'].apply(set).to_dict()

        best_user  = None
        best_score = -1

        for uid, items in user_items.items():
            intersection = len(selected_set & items)
            union        = len(selected_set | items)
            score = intersection / union if union > 0 else 0
            if score > best_score:
                best_score = score
                best_user  = uid

        # Fallback : si aucun livre en commun, trouver le user avec le plus de livres
        # dans les mêmes catégories
        if best_score == 0:
            best_user = df_interactions['u'].value_counts().index[0]

    if best_user is None:
        st.error("Could not find a similar user. Please try different books.")
        return

    # Afficher le profil trouvé
    st.markdown(f"""
        <div style="background:#fff; border-radius:12px; padding:16px 20px;
                    box-shadow:0 4px 12px rgba(0,0,0,0.06); margin-bottom:20px;
                    border-left:4px solid #1f6f43;">
            <p style="font-family:'Playfair Display',serif; color:#1f6f43; font-size:1rem; margin-bottom:4px;">
                ✅ We found your reader twin!
            </p>
            <p style="color:#555; font-size:0.82rem;">
                Based on your <strong>{len(selected_books)} selected books</strong> across
                <strong>{len(selected_cats)} categories</strong>, we matched you with a reader
                who shares similar tastes (similarity score: <strong>{best_score:.1%}</strong>).
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Afficher les recommandations du user jumeau
    from recommendations import afficher_recommandations
    afficher_recommandations(best_user, df_reco, df_enriched)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Start over", use_container_width=True):
            for key in ['cold_start_step', 'cold_start_cats', 'cold_start_books']:
                st.session_state.pop(key, None)
            st.rerun()


# ------------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------------
def afficher_cold_start(df_categories, df_interactions, df_reco, df_enriched):
    if 'cold_start_step' not in st.session_state:
        st.session_state['cold_start_step'] = 1
    if 'cold_start_cats' not in st.session_state:
        st.session_state['cold_start_cats'] = []
    if 'cold_start_books' not in st.session_state:
        st.session_state['cold_start_books'] = []

    step = st.session_state['cold_start_step']

    # Barre de progression
    progress = (step - 1) / 2
    st.markdown(f"""
        <div style="background:#e8f5e9; border-radius:20px; height:8px; margin-bottom:24px; overflow:hidden;">
            <div style="background:#1f6f43; height:100%; width:{int(progress*100)}%;
                        border-radius:20px; transition:width 0.4s ease;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.72rem;
                    color:#aaa; margin-top:-18px; margin-bottom:24px;">
            <span style="color:{'#1f6f43' if step >= 1 else '#aaa'}; font-weight:{'bold' if step==1 else 'normal'}">
                1. Your genres
            </span>
            <span style="color:{'#1f6f43' if step >= 2 else '#aaa'}; font-weight:{'bold' if step==2 else 'normal'}">
                2. Pick books
            </span>
            <span style="color:{'#1f6f43' if step >= 3 else '#aaa'}; font-weight:{'bold' if step==3 else 'normal'}">
                3. Your recommendations
            </span>
        </div>
    """, unsafe_allow_html=True)

    if step == 1:
        step_categories(df_categories)
    elif step == 2:
        step_books(df_categories, df_interactions, df_enriched)
    elif step == 3:
        step_recommendations(df_interactions, df_reco, df_enriched)