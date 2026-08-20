# Book Data Assistant Project
A smaller, beginner-friendly rebuild of a full Databricks and Claude book-data pipeline (ETL, data modeling, star schema, include natural lanquage to SQL agent).

## What this project does
Takes the raw **Goodbooks-10k** dataset, cleans it, models it into a small star schema, and puts a Claude-powered assistant on top that answers plain-English questions about the data by generating and running real SQL.

## Dataset
[Goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k) — ~10,000 books and several million user ratings, originally sourced from Goodreads.

## Architecture
```
books_enriched.csv (Databricks Volume)
        │
        ▼
   1_ETL_script       →  books_simple (cleaned, validated)
        │
        ▼
   2_data_modeling    →  dim_books, book_authors, fact_ratings
        │
        ▼
   Streamlit app (Claude API + Databricks SQL) → ask questions in English
```

## Tables
| Table | Grain | Description |
|---|---|---|
| `dim_books` | one row per book | title, genres, authors, rating, popularity bucket |
| `book_authors` | one row per (book, author) pair | lookup table, since a book can have multiple authors |
| `fact_ratings` | one row per rating | user_id, book_id, rating (1–5) |

## Pipeline steps
1. **ETL** (`1_ETL_script.py`) — reads the raw CSV, checks expected columns exist, casts types, removes rows with a missing `book_id`, removes duplicate `book_id`s, saves as `books_simple`using merge.
2. **Data modeling** (`2_data_modeling.py`) — parses the `genres`/`authors` columns from strings into arrays, adds a derived `popularity_bucket` column, builds `dim_books`, explodes `authors` into a separate `book_authors` table, and builds `fact_ratings` from the raw ratings file.
3. **Agent** (`agent/`) — a Streamlit app: a question is sent to Claude along with a description of the schema, Claude generates SQL, the SQL is checked (only `SELECT` allowed) and run against Databricks. The raw results are sent back to Claude to phrase an answer in English.

## What I'd improve with more time
- Reuse the ETL notebook's `quality_gate` function inside the data modeling notebook, instead of duplicating similar logic
- A composite-key merge for `fact_ratings` (currently keyed just on `book_id`, which isn't unique in that table)
- A small dashboard (Databricks Lakeview) alongside the agent