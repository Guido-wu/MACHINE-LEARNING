import streamlit as st
import pandas as pd
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
        <div style="text-align:center; margin-bottom:24px;">
            <h2 style="font-family:'Playfair Display',serif; color:#1f6f43;">
                What kind of books do you enjoy? 📚
            </h2>
            <p style="color:#666; font-size:0.95rem;">
                Choose <strong>3 categories</strong> that interest you most
            </p>
        </div>
    """, unsafe_allow_html=True)

    all_cats = df_categories['Catégorie'].value_counts()
    all_cats = all_cats[~all_cats.index.isin(['Uncategorized', 'Other'])].index.tolist()
    selected = st.session_state.get('cold_start_cats', [])

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
                        st.warning("Deselect one category first.")
                st.session_state['cold_start_cats'] = selected
                st.rerun()

    st.markdown(f"""
        <div style="text-align:center; margin-top:20px; color:#1f6f43; font-weight:bold;">
            {len(selected)}/3 selected : {' • '.join([CATEGORY_ICONS.get(c,'📚')+' '+c for c in selected])}
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
# ÉTAPE 2 : Sélection des livres — 100% Streamlit natif
# ------------------------------------------------------------------
def step_books(df_categories, df_interactions, df_enriched):
    selected_cats = st.session_state.get('cold_start_cats', [])

    st.markdown(f"""
        <div style="text-align:center; margin-bottom:20px;">
            <h2 style="font-family:'Playfair Display',serif; color:#1f6f43;">
                Which books appeal to you? 👀
            </h2>
            <p style="color:#666; font-size:0.95rem;">
                Click the checkbox under each book — select at least <strong>3</strong><br/>
                <small style="color:#aaa;">
                    {' • '.join([CATEGORY_ICONS.get(c,'📚')+' '+c for c in selected_cats])}
                </small>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Préparer les 20 livres les plus populaires dans les catégories choisies
    df_filtered = df_categories[df_categories['Catégorie'].isin(selected_cats)].copy()
    pop = df_interactions['i'].value_counts().reset_index()
    pop.columns = ['i', 'count']
    df_pop = df_filtered.merge(pop, on='i', how='left').sort_values('count', ascending=False)
    df_pop = df_pop.merge(df_enriched[['i', 'api_thumbnail']], on='i', how='left')

    candidates = []
    for cat in selected_cats:
        candidates.append(df_pop[df_pop['Catégorie'] == cat].head(8))
    df_20 = pd.concat(candidates).drop_duplicates(subset='i').head(20).reset_index(drop=True)

    if 'cold_start_books' not in st.session_state:
        st.session_state['cold_start_books'] = []

    # Affichage en grille 5 colonnes — st.image() evite le bug HTML base64
    N_COLS = 5
    for row_start in range(0, len(df_20), N_COLS):
        row_df = df_20.iloc[row_start:row_start + N_COLS]
        cols   = st.columns(N_COLS)

        for col_idx, (_, book) in enumerate(row_df.iterrows()):
            item_id   = int(book['i'])
            title     = safe_str(book['Title'],  'Unknown')
            author    = safe_str(book['Author'], 'Unknown')
            cat       = safe_str(book['Catégorie'], '')
            icon      = CATEGORY_ICONS.get(cat, '📚')
            is_sel    = item_id in st.session_state['cold_start_books']
            cover_url = safe_cover(book)

            with cols[col_idx]:
                border = "#1f6f43" if is_sel else "rgba(0,0,0,0.08)"
                check_icon = "✅ " if is_sel else ""

                st.markdown(
                    f'<div style="border:3px solid {border};border-radius:10px;overflow:hidden;">',
                    unsafe_allow_html=True
                )

                if cover_url:
                    st.image(cover_url, width=105)
                else:
                    st.markdown(f'''
                        <div style="width:105px;height:150px;background:#1f6f43;
                                    border-radius:8px;display:flex;flex-direction:column;
                                    align-items:center;justify-content:center;gap:6px;">
                            <span style="font-size:1.5rem;">📖</span>
                            <span style="font-size:0.55rem;color:white;text-align:center;
                                         padding:0 6px;line-height:1.3;font-style:italic;">
                                {title[:30]}
                            </span>
                        </div>
                    ''', unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown(
                    f"""<div style="text-align:center;margin-top:2px;margin-bottom:4px;">
                        <span style="font-size:0.58rem;color:#1f6f43;font-weight:bold;">
                            {check_icon}{icon} {cat}</span><br/>
                        <span style="font-size:0.6rem;color:#333;font-style:italic;">
                            {title[:24]}{"..." if len(title)>24 else ""}
                        </span></div>""",
                    unsafe_allow_html=True
                )

                checked = st.checkbox(
                    "select", value=is_sel,
                    key=f"pick_{item_id}",
                    label_visibility="collapsed"
                )

                if checked and item_id not in st.session_state['cold_start_books']:
                    st.session_state['cold_start_books'].append(item_id)
                    st.rerun()
                elif not checked and item_id in st.session_state['cold_start_books']:
                    st.session_state['cold_start_books'].remove(item_id)
                    st.rerun()

        st.divider()

    nb = len(st.session_state['cold_start_books'])

    # Compteur
    st.markdown(f"""
        <div style="text-align:center;margin:12px 0 20px 0;
                    font-family:'Playfair Display',serif;
                    color:#1f6f43;font-size:1rem;font-weight:bold;">
            {'✅' if nb >= 3 else '📚'} {nb} book{'s' if nb != 1 else ''} selected
            {' — ready to go!' if nb >= 3 else f' — select {3 - nb} more to continue'}
        </div>
    """, unsafe_allow_html=True)

    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back"):
            st.session_state['cold_start_step'] = 1
            st.session_state['cold_start_books'] = []
            # Réinitialiser les checkboxes
            for key in list(st.session_state.keys()):
                if key.startswith("pick_"):
                    del st.session_state[key]
            st.rerun()
    with col3:
        if nb >= 3:
            if st.button("✨ Get my recommendations →", use_container_width=True):
                st.session_state['cold_start_step'] = 3
                st.rerun()


# ------------------------------------------------------------------
# ÉTAPE 3 : Similarité Jaccard + recommandations
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
        selected_set = set(selected_books)
        user_items   = df_interactions.groupby('u')['i'].apply(set).to_dict()

        best_user  = None
        best_score = -1

        for uid, items in user_items.items():
            intersection = len(selected_set & items)
            union        = len(selected_set | items)
            score = intersection / union if union > 0 else 0
            if score > best_score:
                best_score = score
                best_user  = uid

        # Fallback si aucun livre en commun
        if best_score == 0:
            best_user = df_interactions['u'].value_counts().index[0]

    if best_user is None:
        st.error("Could not find a similar user. Please try different books.")
        return

    st.markdown(f"""
        <div style="background:#fff;border-radius:12px;padding:16px 20px;
                    box-shadow:0 4px 12px rgba(0,0,0,0.06);margin-bottom:20px;
                    border-left:4px solid #1f6f43;">
            <p style="font-family:'Playfair Display',serif;color:#1f6f43;
                      font-size:1rem;margin-bottom:4px;">✅ We found your reader twin!</p>
            <p style="color:#555;font-size:0.82rem;">
                Based on your <strong>{len(selected_books)} selected books</strong> across
                <strong>{len(selected_cats)} categories</strong>, we matched you with a reader
                who shares similar tastes
                (similarity score: <strong>{best_score:.1%}</strong>).
            </p>
        </div>
    """, unsafe_allow_html=True)

    from recommendations import afficher_recommandations
    afficher_recommandations(best_user, df_reco, df_enriched)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Start over", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith(('cold_start', 'pick_')):
                    del st.session_state[key]
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
        <div style="background:#e8f5e9;border-radius:20px;height:8px;
                    margin-bottom:24px;overflow:hidden;">
            <div style="background:#1f6f43;height:100%;width:{int(progress*100)}%;
                        border-radius:20px;transition:width 0.4s ease;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.72rem;
                    margin-top:-18px;margin-bottom:24px;">
            <span style="color:{'#1f6f43' if step>=1 else '#aaa'};
                         font-weight:{'bold' if step==1 else 'normal'}">1. Your genres</span>
            <span style="color:{'#1f6f43' if step>=2 else '#aaa'};
                         font-weight:{'bold' if step==2 else 'normal'}">2. Pick books</span>
            <span style="color:{'#1f6f43' if step>=3 else '#aaa'};
                         font-weight:{'bold' if step==3 else 'normal'}">3. Recommendations</span>
        </div>
    """, unsafe_allow_html=True)

    if step == 1:
        step_categories(df_categories)
    elif step == 2:
        step_books(df_categories, df_interactions, df_enriched)
    elif step == 3:
        step_recommendations(df_interactions, df_reco, df_enriched)