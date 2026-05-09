# The Bookworm

The Bookworm is a Streamlit book recommender website built around two CSV files:

- `data/final_submission-2.csv`
- `data/items_enriched_api.csv`

It uses the recommendation ids from `final_submission-2.csv` and the enriched book metadata from `items_enriched_api.csv` to create a warm, illustrated reading dashboard with recommendations, exploration, reading goals, stats, friends, and challenge screens.

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── assets/
├── data/
│   ├── final_submission-2.csv
│   └── items_enriched_api.csv
└── src/
    ├── __init__.py
    ├── data_loader.py
    └── ui.py
```

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes

The app is designed to keep working even when some metadata is missing. If a book has no thumbnail, The Bookworm shows a styled cover placeholder using the title.
