"""
schema_context.py (simplified)
--------------------------------
This is just a text description of our database, written so Claude can
read it and understand what tables/columns exist before writing SQL.

No real code logic here -- it's basically documentation that gets pasted
into a prompt.
"""

SCHEMA_CONTEXT = """
Table: dim_books
  book_id (int) - unique id for each book
  title (string)
  genres (array of strings) - e.g. ["Fantasy", "Fiction"]
  average_rating (float)
  ratings_count (int)
  popularity_bucket (int, 1-4)

Table: book_authors
  book_id (int) - matches dim_books.book_id
  author (string)

Table: fact_ratings
  user_id (int)
  book_id (int) - matches dim_books.book_id
  rating (int, 1 to 5)
"""
