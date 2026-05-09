from __future__ import annotations

import html
from typing import Iterable

import pandas as pd
import streamlit as st

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return "" # Si l'image n'est pas trouvée, on ne crash pas







COLORS = {
    "cream": "#fff8e8",
    "paper": "#fffaf0",
    "ink": "#17140f",
    "muted": "#6f685c",
    "green": "#1f6f43",
    "deep": "#083d31",
    "gold": "#f5a623",
    "line": "#eadcc4",
}


def page_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Inter:wght@400;500;600;700&display=swap');

        :root {{
          --cream: {COLORS["cream"]};
          --paper: {COLORS["paper"]};
          --ink: {COLORS["ink"]};
          --muted: {COLORS["muted"]};
          --green: {COLORS["green"]};
          --deep: {COLORS["deep"]};
          --gold: {COLORS["gold"]};
          --line: {COLORS["line"]};
        }}

        .stApp {{
          background:
            radial-gradient(circle at 78% 5%, rgba(245,166,35,.16), transparent 20rem),
            linear-gradient(100deg, #fff3d8 0%, #fffaf0 45%, #fff5df 100%);
          color: var(--ink);
        }}

        section[data-testid="stSidebar"] {{
          background:
            linear-gradient(180deg, rgba(7,57,45,.96), rgba(5,44,36,.98)),
            radial-gradient(circle at 50% 84%, rgba(245,166,35,.24), transparent 12rem);
          border-radius: 0 30px 30px 0;
        }}

        section[data-testid="stSidebar"] * {{
          color: #fff6d6;
        }}

        section[data-testid="stSidebar"] div[role="radiogroup"] label {{
          border-radius: 999px;
          padding: .55rem .7rem;
          margin: .15rem 0;
        }}

        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
          background: rgba(114, 169, 97, .46);
        }}

        .block-container {{
          max-width: 1500px;
          padding: 1.5rem 2rem 2.5rem;
        }}

        h1, h2, h3, .serif {{
          font-family: "Libre Baskerville", Georgia, serif !important;
          letter-spacing: 0;
        }}

        p, div, span, button, input, label {{
          font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        .topbar {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 1rem;
          margin-bottom: 1.15rem;
        }}

        .title h1 {{
          font-size: 2rem;
          margin: 0 0 .25rem;
        }}

        .subtitle {{
          color: var(--muted);
          font-size: 1rem;
        }}

        .card {{
          background: rgba(255, 250, 240, .86);
          border: 1px solid var(--line);
          border-radius: 18px;
          box-shadow: 0 12px 32px rgba(92, 63, 22, .09);
          padding: 1.05rem;
        }}

        .soft-card {{
          background: rgba(255, 252, 244, .72);
          border: 1px solid rgba(234, 220, 196, .88);
          border-radius: 14px;
          padding: .85rem;
        }}

        .metric-row {{
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: .85rem;
        }}

        .metric {{
          display: flex;
          align-items: center;
          gap: .75rem;
          border-right: 1px solid var(--line);
          min-height: 78px;
        }}

        .metric:last-child {{
          border-right: 0;
        }}

        .metric-icon {{
          width: 48px;
          height: 48px;
          display: grid;
          place-items: center;
          border-radius: 14px;
          background: #f7edcc;
          font-size: 1.45rem;
        }}

        .metric strong {{
          display: block;
          font-size: 1.55rem;
          color: var(--ink);
        }}

        .book-grid {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(132px, 1fr));
          gap: .95rem;
        }}

        .book-card {{
          min-width: 0;
        }}

        .cover {{
          width: 100%;
          aspect-ratio: 2 / 3;
          object-fit: cover;
          border-radius: 8px;
          box-shadow: 0 12px 22px rgba(25, 20, 14, .18);
          background: linear-gradient(145deg, #143d38, #f0c66a);
        }}

        .cover-placeholder {{
          width: 100%;
          aspect-ratio: 2 / 3;
          border-radius: 8px;
          box-shadow: 0 12px 22px rgba(25, 20, 14, .16);
          background:
            linear-gradient(145deg, rgba(8,61,49,.96), rgba(20,94,62,.82)),
            radial-gradient(circle at 50% 18%, rgba(245,166,35,.35), transparent 4rem);
          color: #fff4c8;
          display: flex;
          align-items: center;
          justify-content: center;
          text-align: center;
          padding: .75rem;
          font-family: "Libre Baskerville", Georgia, serif;
          font-weight: 700;
        }}

        .book-title {{
          font-weight: 700;
          font-size: .9rem;
          margin-top: .6rem;
          line-height: 1.2;
        }}

        .book-author, .tiny {{
          color: var(--muted);
          font-size: .78rem;
          line-height: 1.35;
        }}

        .stars {{
          color: #ef7d18;
          letter-spacing: .05rem;
          font-size: .78rem;
          margin-top: .25rem;
        }}

        .pill-row {{
          display: flex;
          gap: .6rem;
          flex-wrap: wrap;
        }}

        .pill {{
          border: 1px solid var(--line);
          border-radius: 999px;
          padding: .55rem .85rem;
          background: rgba(255,255,255,.45);
          font-weight: 600;
          font-size: .88rem;
        }}

        .pill.active {{
          background: var(--green);
          color: white;
          border-color: var(--green);
        }}

        .mascot {{
          min-height: 260px;
          display: grid;
          place-items: center;
          text-align: center;
          background:
            radial-gradient(circle at 50% 55%, rgba(245,166,35,.22), transparent 9rem),
            linear-gradient(180deg, rgba(255,252,244,.85), rgba(255,243,218,.8));
          overflow: hidden;
        }}

        .worm {{
          font-size: 6.5rem;
          line-height: 1;
          filter: drop-shadow(0 18px 18px rgba(69, 44, 12, .18));
        }}

        .stack {{
          font-size: 3.2rem;
          margin-top: -.8rem;
        }}

        .dark-band {{
          background: linear-gradient(100deg, #073d31, #1f6f43);
          color: #fff5cf;
          border-radius: 16px;
          padding: 1.25rem 1.4rem;
          overflow: hidden;
        }}

        .dark-band h2, .dark-band p {{
          color: #fff5cf;
        }}

        .friend-row {{
          display: grid;
          grid-template-columns: 38px 1fr auto;
          align-items: center;
          gap: .65rem;
          padding: .45rem 0;
        }}

        .avatar {{
          width: 38px;
          height: 38px;
          display: grid;
          place-items: center;
          border-radius: 50%;
          background: #f4dcb4;
          font-size: 1.25rem;
        }}

        .green-button {{
          background: var(--green);
          color: white;
          border-radius: 999px;
          padding: .45rem .85rem;
          font-weight: 700;
          font-size: .8rem;
        }}

        .progress-bar {{
          height: 8px;
          border-radius: 999px;
          background: #e7dcc7;
          overflow: hidden;
          margin-top: .45rem;
        }}

        .progress-fill {{
          height: 100%;
          background: linear-gradient(90deg, var(--green), #f29b2f);
          border-radius: 999px;
        }}

        @media (max-width: 900px) {{
          .metric-row {{
            grid-template-columns: repeat(2, minmax(0, 1fr));
          }}
          .metric {{
            border-right: 0;
          }}
          .topbar {{
            display: block;
          }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar(active: str) -> str:

  logo_path = "a9e8a2a7-e0a4-422d-b5a9-57ae442fb57a.png"

  st.sidebar.markdown(
      f"""
      <style>
            /* Cache le petit point rouge du bouton radio */
            [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {{
                display: none !important;
            }}
            /* Style pour que le texte soit bien centré sans le point */
            [data-testid="stSidebar"] div[role="radiogroup"] label {{
                padding-left: 15px !important;
            }}


      <div style="padding:1.2rem .8rem 1.6rem;text-align:center">
          <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{get_image_base64(logo_path)}" 
                 style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover;">
          </div>
          <div class="serif" style="font-size:2rem;font-weight:700;line-height:1.05">The<br>Bookworm</div>
          <div style="margin-top:.8rem;font-size:.95rem;color:#fff0bc">Dive into stories.<br>Grow your world.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  pages = [
        "Home",
        "My Library",
        "Recommendations",
        "Explore",
        "Reading Goals",
        "Stats & Insights",
        "Friends",
        "Challenges",
        "Bookmarks",
    ]
  choice = st.sidebar.radio("Navigation", pages, index=pages.index(active), label_visibility="collapsed")
  st.sidebar.markdown(
        """
        <div style="height:14rem"></div>
        <div style="padding:1rem;text-align:center">
          <div style="font-size:4rem">☕</div>
          <div style="font-size:.85rem;color:#fff0bc">just one<br>more chapter</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  return choice


def header(title: str, subtitle: str, search_label: str = "Search for books, authors, genres...") -> str:
    st.markdown(
        f"""
        <div class="topbar">
          <div class="title">
            <h1>{html.escape(title)} <span style="color:#2f7b4c">⌁</span></h1>
            <div class="subtitle">{html.escape(subtitle)}</div>
          </div>
          <div style="display:flex;gap:.8rem;align-items:center">
            <div class="soft-card" style="padding:.55rem 1rem">🔔</div>
            <div class="soft-card" style="padding:.55rem 1rem">🔥 <b>12</b></div>
            <div class="avatar">👩</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return st.text_input(search_label, placeholder=search_label, label_visibility="collapsed")


def card_start(classes: str = "card") -> None:
    st.markdown(f'<div class="{classes}">', unsafe_allow_html=True)


def card_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def cover_html(book: pd.Series) -> str:
    title = html.escape(str(book.get("clean_title", book.get("title", "Book"))))
    cover = str(book.get("cover", "")).strip()
    if cover.startswith("http"):
        return f'<img class="cover" src="{html.escape(cover)}" alt="{title} cover">'
    return f'<div class="cover-placeholder">{title}</div>'


def book_grid(books: pd.DataFrame, limit: int = 5, descriptions: bool = False) -> None:
    items = []
    for _, book in books.head(limit).iterrows():
        title = html.escape(str(book.get("clean_title", book.get("title", "Untitled Book"))))
        author = html.escape(str(book.get("author", "Unknown author")))
        desc = html.escape(str(book.get("description", "")))
        description_html = f'<div class="book-author" style="margin-top:.45rem">{desc}</div>' if descriptions else ""
        items.append(
            f"""
            <div class="book-card">
              {cover_html(book)}
              <div class="book-title">{title}</div>
              <div class="book-author">{author}</div>
              <div class="stars">★★★★★</div>
              {description_html}
            </div>
            """
        )
    st.markdown(f'<div class="book-grid">{"".join(items)}</div>', unsafe_allow_html=True)


def mascot_card(title: str = "Your Bookworm", text: str = "Customize your bookish buddy!") -> None:
    st.markdown(
        f"""
        <div class="card mascot">
          <div>
            <h3 style="margin:.1rem 0 .25rem">{html.escape(title)}</h3>
            <div class="tiny">{html.escape(text)}</div>
            <div class="worm">🐛</div>
            <div class="stack">📚✨</div>
            <div class="pill-row" style="justify-content:center;margin-top:.8rem">
              <span class="pill active">👓</span><span class="pill">🧙</span><span class="pill">🎩</span><span class="pill">🧣</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_row(metrics: Iterable[tuple[str, str, str]]) -> None:
    html_metrics = []
    for icon, value, label in metrics:
        html_metrics.append(
            f"""
            <div class="metric">
              <div class="metric-icon">{html.escape(icon)}</div>
              <div><strong>{html.escape(value)}</strong><span class="tiny">{html.escape(label)}</span></div>
            </div>
            """
        )
    st.markdown(f'<div class="card metric-row">{"".join(html_metrics)}</div>', unsafe_allow_html=True)
