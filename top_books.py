import streamlit as st
import pandas as pd
import base64

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def safe_str(val, fallback='Unknown'):
    """Convertit proprement une valeur pandas en string, gère NaN."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return fallback
    return str(val)

def safe_cover(row, col='api_thumbnail'):
    """Retourne l'URL de cover si valide, sinon None."""
    val = row[col] if col in row.index else None
    if val is None or (isinstance(val, float) and pd.isna(val)) or str(val).strip() == '':
        return None
    return str(val)

# ---------------------------------------------------------
# FALLBACK COVER : SVG encodé en base64
# ---------------------------------------------------------
def generate_fallback_cover(title, author, rank=None):
    title  = safe_str(title, 'Unknown Title')
    author = safe_str(author, 'Unknown')

    short_title  = title[:35]  + "…" if len(title)  > 35 else title
    short_author = author[:25] + "…" if len(author) > 25 else author

    # Échapper les caractères XML dangereux
    short_title  = short_title.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
    short_author = short_author.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

    medal    = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "")
    bg_color = {1: "#b8860b", 2: "#708090", 3: "#8B4513"}.get(rank, "#1f6f43")

    # SVG pur (pas de foreignObject qui pose problème dans certains navigateurs)
    lines = []
    words = short_title.split()
    line, line_len = "", 0
    for w in words:
        if line_len + len(w) > 16:
            lines.append(line.strip())
            line, line_len = w + " ", len(w) + 1
        else:
            line += w + " "
            line_len += len(w) + 1
    if line.strip():
        lines.append(line.strip())
    lines = lines[:4]

    title_svg = ""
    for i, l in enumerate(lines):
        title_svg += f'<text x="70" y="{75 + i*16}" font-family="Georgia,serif" font-size="10" font-weight="bold" fill="white" text-anchor="middle">{l}</text>\n'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="140" height="200" viewBox="0 0 140 200">
  <rect width="140" height="200" rx="8" fill="{bg_color}"/>
  <rect x="6" y="6" width="128" height="188" rx="6" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
  <text x="70" y="55" font-family="Georgia,serif" font-size="24" fill="white" text-anchor="middle">{medal if medal else "📖"}</text>
  {title_svg}
  <line x1="20" y1="162" x2="120" y2="162" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="70" y="178" font-family="Georgia,serif" font-size="9" font-style="italic" fill="rgba(255,255,255,0.8)" text-anchor="middle">{short_author}</text>
</svg>'''

    b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64}"


# ---------------------------------------------------------
# TOP 3 BOOKS — PODIUM
# ---------------------------------------------------------
def afficher_top_books(df_enriched, df_interactions):
    top_ids = df_interactions['i'].value_counts().head(3).reset_index()
    top_ids.columns = ['i', 'count']
    top_books = top_ids.merge(df_enriched[['i', 'Title', 'Author', 'api_thumbnail']], on='i', how='left')

    podium_order  = [1, 0, 2]
    podium_heights = ["160px", "210px", "130px"]
    podium_colors  = ["#9e9e9e", "#b8860b", "#8B4513"]
    podium_labels  = ["🥈 2nd", "🥇 1st", "🥉 3rd"]
    podium_ranks   = [2, 1, 3]

    st.markdown("""
    <style>
    .podium-wrapper { display:flex; justify-content:center; align-items:flex-end; gap:20px; margin:10px 0; }
    .podium-item    { display:flex; flex-direction:column; align-items:center; gap:8px; }
    .podium-cover   { border-radius:10px; box-shadow:0 8px 20px rgba(0,0,0,0.2); object-fit:cover; transition:transform .2s; }
    .podium-cover:hover { transform:scale(1.05); }
    .podium-base    { border-radius:10px 10px 0 0; display:flex; align-items:center; justify-content:center;
                      font-weight:bold; color:white; font-family:'Playfair Display',serif; font-size:.85rem; width:120px; }
    .podium-title   { font-size:.72rem; color:#444; text-align:center; max-width:130px; line-height:1.3; font-style:italic; }
    .podium-count   { font-size:.68rem; color:#1f6f43; font-weight:bold; }
    </style>
    """, unsafe_allow_html=True)

    html = '<div class="podium-wrapper">'
    for pos, idx in enumerate(podium_order):
        if idx >= len(top_books):
            continue
        row    = top_books.iloc[idx]
        rank   = podium_ranks[pos]
        height = podium_heights[pos]
        color  = podium_colors[pos]
        label  = podium_labels[pos]

        cover = safe_cover(row)
        if not cover:
            cover = generate_fallback_cover(row['Title'], row['Author'], rank)

        short_title = safe_str(row['Title'])[:30] + "…" if len(safe_str(row['Title'])) > 30 else safe_str(row['Title'])

        html += f"""
        <div class="podium-item">
            <img src="{cover}" width="110" height="155" class="podium-cover"/>
            <span class="podium-title">{short_title}</span>
            <span class="podium-count">📖 {int(row['count'])} reads</span>
            <div class="podium-base" style="background-color:{color};height:{height};">{label}</div>
        </div>"""

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------
# NEW RELEASES
# ---------------------------------------------------------
def afficher_new_releases(df_enriched):
    df = df_enriched.copy()
    df['year'] = pd.to_numeric(df['api_published_date'].str[:4], errors='coerce')
    df_recent = df[df['year'] >= 2022].sort_values('year', ascending=False)
    top_recent = df_recent.head(20).drop_duplicates(subset='Title').head(6)

    st.markdown("""
    <style>
    .releases-grid { display:flex; flex-wrap:wrap; gap:16px; justify-content:flex-start; margin-top:10px; }
    .release-card  { display:flex; flex-direction:column; align-items:center; gap:6px; width:110px; }
    .release-cover { border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.15); object-fit:cover; transition:transform .2s; }
    .release-cover:hover { transform:scale(1.05); }
    .release-title { font-size:.7rem; color:#333; text-align:center; font-style:italic; line-height:1.3; }
    .release-year  { font-size:.65rem; color:#1f6f43; font-weight:bold; }
    </style>
    """, unsafe_allow_html=True)

    html = '<div class="releases-grid">'
    for _, row in top_recent.iterrows():
        cover = safe_cover(row)
        if not cover:
            cover = generate_fallback_cover(row['Title'], row['Author'])

        short_title = safe_str(row['Title'])
        short_title = short_title[:28] + "…" if len(short_title) > 28 else short_title
        year = int(row['year']) if not pd.isna(row['year']) else "?"

        html += f"""
        <div class="release-card">
            <img src="{cover}" width="100" height="145" class="release-cover"/>
            <span class="release-title">{short_title}</span>
            <span class="release-year">✨ {year}</span>
        </div>"""

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)