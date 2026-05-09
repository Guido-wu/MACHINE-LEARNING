from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ITEMS_PATH = DATA_DIR / "items_enriched_api.csv"
RECOMMENDATIONS_PATH = DATA_DIR / "final_submission-2.csv"


def _clean_text(value: object, fallback: str = "") -> str:
    if pd.isna(value):
        return fallback
    text = str(value).strip()
    if text.lower() in {"nan", "none", "null", "[]"}:
        return fallback
    return text


def _shorten(text: str, length: int = 150) -> str:
    text = " ".join(_clean_text(text).split())
    if len(text) <= length:
        return text
    return text[: length - 1].rstrip() + "..."


def _title_case(value: str) -> str:
    value = _clean_text(value)
    return value if value else "Untitled Book"


def _author_name(row: pd.Series) -> str:
    return _clean_text(row.get("api_authors")) or _clean_text(row.get("Author")) or "Unknown author"


def _category(row: pd.Series) -> str:
    for column in ("api_categories", "categories", "Subjects"):
        value = _clean_text(row.get(column))
        if value:
            value = value.replace("[", "").replace("]", "").replace("'", "")
            return value.split(";")[0].split(",")[0].strip() or "General"
    return "General"


def _description(row: pd.Series) -> str:
    for column in ("api_description", "description_x", "description_y"):
        value = _clean_text(row.get(column))
        if value:
            return _shorten(value, 190)
    return "A promising read from The Bookworm collection, ready for your next chapter."


def _rating(index: int) -> float:
    return round(4.1 + ((index * 7) % 9) / 10, 1)


@pd.api.extensions.register_dataframe_accessor("bookworm")
class _BookwormAccessor:
    def __init__(self, pandas_obj: pd.DataFrame) -> None:
        self._obj = pandas_obj

    def sample_books(self, count: int, offset: int = 0) -> pd.DataFrame:
        if self._obj.empty:
            return self._obj
        start = offset % len(self._obj)
        order = list(range(start, len(self._obj))) + list(range(0, start))
        return self._obj.iloc[order].head(count)


def load_books(path: Path = ITEMS_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing book data: {path}")

    raw = pd.read_csv(path)
    item_ids = pd.to_numeric(raw.get("i"), errors="coerce")
    item_ids = item_ids.fillna(pd.Series(raw.index, index=raw.index)).astype(int)

    books = pd.DataFrame(
        {
            "item_id": item_ids,
            "title": raw.apply(
                lambda row: _clean_text(row.get("api_title")) or _title_case(row.get("Title")),
                axis=1,
            ),
            "author": raw.apply(_author_name, axis=1),
            "publisher": raw.get("api_publisher", raw.get("Publisher", "")).fillna(""),
            "year": raw.get("api_published_date", "").fillna("").astype(str).str[:4],
            "category": raw.apply(_category, axis=1),
            "description": raw.apply(_description, axis=1),
            "cover": raw.get("api_thumbnail", "").fillna(""),
            "isbn": raw.get("isbn_clean", "").fillna("").astype(str),
            "all_text": raw.get("all_text", "").fillna("").astype(str),
        }
    )
    books["rating"] = [_rating(i) for i in range(len(books))]
    books["pages"] = 120 + (books["item_id"] * 17) % 780
    books["clean_title"] = books["title"].str.replace(r"\s*/$", "", regex=True).str.strip()
    return books.drop_duplicates("item_id").reset_index(drop=True)


def load_recommendations(path: Path = RECOMMENDATIONS_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing recommendation data: {path}")
    recs = pd.read_csv(path)
    recs["recommendation_ids"] = recs["recommendation"].fillna("").apply(
        lambda value: [int(item) for item in str(value).split() if item.isdigit()]
    )
    return recs


def recommendations_for_user(books: pd.DataFrame, recs: pd.DataFrame, user_id: int = 0) -> pd.DataFrame:
    if recs.empty:
        return books.bookworm.sample_books(10)
    row = recs.loc[recs["user_id"] == user_id]
    if row.empty:
        row = recs.head(1)
    ids: Iterable[int] = row.iloc[0]["recommendation_ids"]
    selected = books[books["item_id"].isin(ids)].copy()
    selected["_rank"] = selected["item_id"].map({item_id: i for i, item_id in enumerate(ids)})
    return selected.sort_values("_rank").drop(columns=["_rank"])


def search_books(books: pd.DataFrame, query: str, limit: int = 12) -> pd.DataFrame:
    query = query.strip().lower()
    if not query:
        return books.bookworm.sample_books(limit)
    haystack = (
        books["title"].fillna("")
        + " "
        + books["author"].fillna("")
        + " "
        + books["category"].fillna("")
        + " "
        + books["all_text"].fillna("")
    ).str.lower()
    return books[haystack.str.contains(query, regex=False)].head(limit)


def genre_options(books: pd.DataFrame, limit: int = 9) -> list[str]:
    values = (
        books["category"]
        .dropna()
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    values = values[values.ne("") & values.ne("General")]
    return values.value_counts().head(limit).index.tolist()
