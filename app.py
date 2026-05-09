from __future__ import annotations

import random

import pandas as pd
import streamlit as st

from src.data_loader import (
    genre_options,
    load_books,
    load_recommendations,
    recommendations_for_user,
    search_books,
)
from src.ui import (
    book_grid,
    card_end,
    card_start,
    header,
    mascot_card,
    metric_row,
    page_css,
    sidebar,
)


st.set_page_config(
    page_title="The Bookworm",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def get_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    return load_books(), load_recommendations()


def recommendation_pool(books: pd.DataFrame, recs: pd.DataFrame) -> pd.DataFrame:
    user_id = st.session_state.get("user_id", 0)
    rec_books = recommendations_for_user(books, recs, user_id=user_id)
    if len(rec_books) < 10:
        rec_books = pd.concat([rec_books, books.bookworm.sample_books(10, offset=28)]).drop_duplicates("item_id")
    return rec_books


def show_home(books: pd.DataFrame, recs: pd.DataFrame) -> None:
    query = header("Welcome back, Alex!", "What chapter will you write today?")
    rec_books = search_books(recommendation_pool(books, recs), query, 10) if query else recommendation_pool(books, recs)

    left, mid, right = st.columns([1.15, 1.15, .9], gap="large")
    with left:
        card_start()
        st.markdown("### 1. Add Books You Have Read")
        st.caption("Help us learn your taste.")
        title = st.text_input("Search a book title or author", placeholder="Search a book title or author")
        if title:
            book_grid(search_books(books, title, 3), limit=3)
        else:
            st.markdown(
                """
                <div style="display:flex;align-items:center;gap:1.2rem;min-height:180px">
                  <div style="font-size:6rem">🐛</div>
                  <div style="flex:1">
                    <div class="soft-card" style="border-style:dashed;text-align:center;padding:1rem">
                      Search above or add from your library
                    </div>
                    <div style="margin-top:1rem;text-align:center">
                      <span class="green-button">📖 Add from your library</span>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        card_end()

        st.write("")
        card_start()
        st.markdown("### 3. 2025 Reading Goal")
        st.caption("You are doing amazing.")
        st.markdown(
            """
            <div style="display:grid;place-items:center;padding:1rem 0">
              <div style="width:190px;height:190px;border-radius:50%;border:18px solid #e9dfca;border-top-color:#1f6f43;border-right-color:#1f6f43;display:grid;place-items:center">
                <div style="text-align:center"><div class="serif" style="font-size:3.2rem;font-weight:700">24</div><div>of 50 books</div></div>
              </div>
              <div class="tiny" style="margin-top:.85rem">48% complete</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.success("Keep going! 📚")
        card_end()

    with mid:
        card_start()
        cols = st.columns([.8, .2])
        with cols[0]:
            st.markdown("### 2. Your Recommendations")
            st.caption("Picked just for you.")
        with cols[1]:
            st.link_button("View all", "#")
        book_grid(rec_books, limit=4)
        card_end()

        st.write("")
        c1, c2 = st.columns([.9, 1.1], gap="medium")
        with c1:
            card_start()
            st.markdown("### 4. Quote of the Day")
            st.markdown(
                """
                <div class="serif" style="font-size:1.35rem;line-height:1.45;margin:1rem 0">
                  "A book is a dream that you hold in your hands."
                </div>
                <div class="tiny">Neil Gaiman</div>
                """,
                unsafe_allow_html=True,
            )
            card_end()
        with c2:
            card_start()
            st.markdown("### 5. Fun Fact")
            st.write("George Orwell's *1984* was inspired by a fear of totalitarianism and written in just one year.")
            st.button("Tell me more!", use_container_width=True)
            card_end()

        st.write("")
        st.markdown(
            """
            <div class="dark-band">
              <h2 style="margin:.1rem 0 .35rem">6. Summer Vibes ☀️</h2>
              <p>Sunshine reads for long days and warm nights.</p>
              <span class="green-button" style="background:#fff5cf;color:#1f6f43">Explore picks →</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        mascot_card()
        st.write("")
        card_start()
        st.markdown("### Friend Activity")
        friend_activity = rec_books.bookworm.sample_books(3, offset=2)
        friends = ["Sophie just finished", "Liam is reading", "Maya wants to read"]
        for label, (_, book) in zip(friends, friend_activity.iterrows()):
            st.markdown(f"**{label}**")
            st.caption(f"{book['clean_title']} · {book['author']}")
        card_end()


def show_recommendations(books: pd.DataFrame, recs: pd.DataFrame) -> None:
    query = header("Find your next great read", "Tell us what you have read and how you are feeling.")
    rec_books = recommendation_pool(books, recs)

    main, side = st.columns([1.9, .85], gap="large")
    with main:
        card_start()
        st.markdown("### 1. Add books you have read")
        selected = rec_books.head(5)
        book_grid(selected, limit=5)
        card_end()

        st.write("")
        card_start()
        st.markdown("### 2. What are you in the mood for?")
        moods = ["☕ Cozy", "⛰ Adventurous", "♡ Heartwarming", "🧠 Thought-provoking", "🙂 Funny", "🔍 Mysterious"]
        st.markdown(
            '<div class="pill-row">' + "".join(f'<span class="pill {"active" if i in (0, 2) else ""}">{m}</span>' for i, m in enumerate(moods)) + "</div>",
            unsafe_allow_html=True,
        )
        card_end()

        st.write("")
        card_start()
        st.markdown("### 3. Refine your taste")
        genres = genre_options(books, 8)
        if genres:
            st.markdown(
                '<div class="pill-row">' + "".join(f'<span class="pill {"active" if i == 0 else ""}">{g}</span>' for i, g in enumerate(genres)) + "</div>",
                unsafe_allow_html=True,
            )
        card_end()

        st.write("")
        card_start()
        st.markdown("### Your recommendations")
        st.caption("Based on your books, mood, and taste.")
        pool = search_books(books, query, 8) if query else rec_books
        book_grid(pool, limit=5, descriptions=True)
        card_end()

    with side:
        st.markdown(
            """
            <div class="card" style="text-align:center">
              <div class="soft-card" style="margin-bottom:1rem">I've got some wonderful recommendations for you! Let's find your next favorite book.</div>
              <div class="worm">🐛</div>
              <div class="stack">📚</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        card_start()
        st.markdown("### Because you loved...")
        if len(rec_books):
            book_grid(rec_books.head(4), limit=4)
        card_end()
        st.write("")
        card_start()
        st.markdown("### Winter Cozy Reads")
        cozy = books[books["all_text"].str.contains("snow|winter|cozy|moon", case=False, regex=True, na=False)]
        book_grid(cozy if not cozy.empty else books.bookworm.sample_books(4, 80), limit=4)
        card_end()


def show_stats(books: pd.DataFrame, recs: pd.DataFrame) -> None:
    header("Your 2025 in Books", "A year well read. A story well lived.")
    rec_books = recommendation_pool(books, recs)

    st.markdown(
        """
        <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem">
          <div>
            <div class="serif" style="font-size:4.8rem;line-height:1;font-weight:700">Your <span style="color:#1f6f43">2025</span><br>in Books</div>
            <div class="subtitle" style="margin-top:.8rem">A year well read. A story well lived.</div>
          </div>
          <div style="font-size:7rem">🐛🎉</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    metric_row(
        [
            ("📗", "24", "Books Read"),
            ("📄", "8,742", "Pages Read"),
            ("🕒", "312", "Hours Read"),
            ("⭐", "4.8", "Average Rating"),
        ]
    )
    st.write("")

    left, right = st.columns([1.9, .85], gap="large")
    with left:
        c1, c2, c3, c4 = st.columns(4)
        tiles = [
            ("Favorite Author", rec_books.iloc[0]["author"] if len(rec_books) else "Taylor Jenkins Reid", "3 books read", "👩"),
            ("Favorite Genre", rec_books.iloc[0]["category"] if len(rec_books) else "Historical Fiction", "9 books", "🏰"),
            ("Longest Book", rec_books.iloc[1]["clean_title"] if len(rec_books) > 1 else "The Pillars of the Earth", "973 pages", "⛪"),
            ("Shortest Book", rec_books.iloc[2]["clean_title"] if len(rec_books) > 2 else "The Little Prince", "96 pages", "🌟"),
        ]
        for col, (label, value, caption, icon) in zip([c1, c2, c3, c4], tiles):
            with col:
                card_start()
                st.markdown(f"#### {label}")
                st.markdown(f"### {value}")
                st.caption(caption)
                st.markdown(f"<div style='font-size:3.5rem;text-align:center'>{icon}</div>", unsafe_allow_html=True)
                card_end()

        st.write("")
        c1, c2, c3, c4 = st.columns(4)
        for col, data in zip(
            [c1, c2, c3, c4],
            [("Reading Streak", "🔥 145", "days in a row"), ("Best Month", "September", "6 books read"), ("Most Read Day", "Saturday", "8 books"), ("Top Mood", "Adventurous", "✨")],
        ):
            with col:
                card_start()
                st.markdown(f"#### {data[0]}")
                st.markdown(f"### {data[1]}")
                st.caption(data[2])
                card_end()

        st.write("")
        st.markdown(
            """
            <div class="dark-band">
              <h2>You turned pages into memories this year.</h2>
              <p>Here is to more stories in 2026.</p>
              <span class="green-button" style="background:#fff5cf;color:#1f6f43">Set a 2026 Goal</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        card_start()
        st.markdown("### Share Your Year")
        st.caption("Celebrate your reading journey with friends.")
        st.markdown(
            """
            <div style="background:#073d31;color:#fff5cf;border-radius:14px;padding:1.2rem;text-align:center">
              <div class="serif" style="font-size:2.2rem;color:#f8cb74">My 2025<br>in Books</div>
              <div style="font-size:5rem">🐛</div>
              <div style="display:flex;justify-content:space-around">
                <b>24<br><span class="tiny">Books</span></b>
                <b>8,742<br><span class="tiny">Pages</span></b>
                <b>145<br><span class="tiny">Streak</span></b>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("Share My Recap", use_container_width=True)
        st.download_button("Download", "The Bookworm 2025 recap", file_name="bookworm-recap.txt", use_container_width=True)
        card_end()

        st.write("")
        card_start()
        st.markdown("### Top Picks for Your Next Chapter")
        book_grid(rec_books, limit=5)
        card_end()


def show_friends(books: pd.DataFrame, recs: pd.DataFrame) -> None:
    header("Friends & Community", "Stories are better together.", "Search friends, clubs, or challenges...")
    rec_books = recommendation_pool(books, recs)

    left, center, right = st.columns([.8, 2.45, 1.15], gap="medium")
    with left:
        card_start()
        st.markdown("### Add Friends")
        for name, emoji, mutual in [
            ("Sophie Luu", "👩", 12),
            ("Ethan Park", "👨", 8),
            ("Isabella Rossi", "👩", 5),
            ("Noah Bennett", "👨", 7),
        ]:
            st.markdown(
                f"""
                <div class="friend-row">
                  <div class="avatar">{emoji}</div>
                  <div><b>{name}</b><div class="tiny">{mutual} mutual friends</div></div>
                  <span class="green-button">Add</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        card_end()
        st.write("")
        card_start()
        st.markdown("### Reading Streak")
        st.markdown("<div style='font-size:3rem;text-align:center'>🔥 <b>12</b></div>", unsafe_allow_html=True)
        st.caption("days in a row")
        st.progress(.82)
        card_end()
        st.write("")
        card_start()
        st.markdown("### Compare Goals")
        st.metric("You", "24 of 50 books")
        st.metric("Sophie Luu", "31 of 50 books")
        card_end()

    with center:
        card_start()
        st.markdown("### What Your Friends Are Reading")
        book_grid(rec_books, limit=5)
        card_end()
        st.write("")
        card_start()
        st.markdown("### Community Feed")
        st.text_input("Share a thought, review, or recommendation...", label_visibility="collapsed")
        for name, action, book in [
            ("Sophie Luu", "reviewed", rec_books.iloc[0] if len(rec_books) else books.iloc[0]),
            ("Maya Evans", "commented on", rec_books.iloc[1] if len(rec_books) > 1 else books.iloc[1]),
            ("Ethan Park", "added", rec_books.iloc[2] if len(rec_books) > 2 else books.iloc[2]),
        ]:
            st.markdown(f"**{name}** {action} **{book['clean_title']}**")
            st.caption(book["description"])
        card_end()

    with right:
        mascot_card("Customize Your Bookworm", "Dress your worm for every adventure!")
        st.write("")
        card_start()
        st.markdown("### Book Clubs")
        for club, members in [("Fantasy Fellowship", "1.2K"), ("The Cozy Corner", "856"), ("Sci-Fi Explorers", "1.5K")]:
            st.markdown(f"**{club}**")
            st.caption(f"{members} members")
        card_end()
        st.write("")
        card_start()
        st.markdown("### Active Challenges")
        for challenge, score in [("Summer Reading Sprint", "1.1K"), ("Read Around the World", "842"), ("Series Finisher", "623")]:
            st.markdown(f"**{challenge}**")
            st.caption(score)
        card_end()


def show_library(books: pd.DataFrame) -> None:
    query = header("My Library", "Your saved shelves, favorites, and future chapters.")
    results = search_books(books, query, 16) if query else books.bookworm.sample_books(16, 120)
    st.markdown("### Saved Books")
    book_grid(results, limit=8, descriptions=True)


def show_explore(books: pd.DataFrame) -> None:
    query = header("Explore", "Browse the full Bookworm collection.")
    genres = genre_options(books, 12)
    st.markdown('<div class="pill-row">' + "".join(f'<span class="pill">{g}</span>' for g in genres) + "</div>", unsafe_allow_html=True)
    st.write("")
    results = search_books(books, query, 18) if query else books.bookworm.sample_books(18, 260)
    book_grid(results, limit=10, descriptions=True)


def show_simple_page(title: str, subtitle: str, books: pd.DataFrame, offset: int) -> None:
    header(title, subtitle)
    left, right = st.columns([1.6, .9], gap="large")
    with left:
        metric_row([("📚", "24", "Books"), ("🔥", "12", "Day Streak"), ("⭐", "4.8", "Avg Rating"), ("🏆", "6", "Badges")])
        st.write("")
        card_start()
        st.markdown("### Featured Reads")
        book_grid(books.bookworm.sample_books(6, offset), limit=6)
        card_end()
    with right:
        mascot_card(title, subtitle)


def main() -> None:
    page_css()
    try:
        books, recs = get_data()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.info("Place final_submission-2.csv and items_enriched_api.csv inside the data folder, then restart the app.")
        return

    st.session_state.setdefault("user_id", 0)
    page = sidebar("Home")

    if page == "Home":
        show_home(books, recs)
    elif page == "Recommendations":
        show_recommendations(books, recs)
    elif page == "Stats & Insights":
        show_stats(books, recs)
    elif page == "Friends":
        show_friends(books, recs)
    elif page == "My Library":
        show_library(books)
    elif page == "Explore":
        show_explore(books)
    elif page == "Reading Goals":
        show_simple_page("Reading Goals", "Track the chapters you promised yourself.", books, 430)
    elif page == "Challenges":
        show_simple_page("Challenges", "Join seasonal quests and collect badges.", books, 620)
    elif page == "Bookmarks":
        show_simple_page("Bookmarks", "Return to books that caught your eye.", books, 840)


if __name__ == "__main__":
    random.seed(7)
    main()
