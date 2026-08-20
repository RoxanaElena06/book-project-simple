import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from nl_to_sql import question_to_sql, phrase_answer
from execute_sql import execute_query, get_table_preview

#Page setup
st.set_page_config(
    page_title="Book Data Assistant (Simplified)",
    page_icon="📚",
    layout="centered"
)
 
#Basic custom styling
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .subtitle {
        color: #9aa0a6;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .example-questions {
        color: #9aa0a6;
        font-size: 0.9rem;
    }
    .section-header {
        margin-top: 2.5rem;
        border-top: 1px solid #262730;
        padding-top: 1.5rem;
    }
    .footer-note {
        color: #6b7280;
        font-size: 0.8rem;
        margin-top: 3rem;
        border-top: 1px solid #262730;
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)
 
#Header / intro
st.title("📚 Book Data Assistant")
st.markdown(
    '<p class="subtitle">Ask a question about the book dataset in plain English.</p>',
    unsafe_allow_html=True
)
 
#Example questions
st.markdown('<p class="example-questions">Try one of these, or ask your own:</p>', unsafe_allow_html=True)
 
example_questions = [
    "Which genre has the highest average rating?",
    "Who are the most prolific authors?",
    "What is the total number of books in the database?",
    "Does page count relate to rating?",
]
 
if "question_input" not in st.session_state:
    st.session_state.question_input = ""
 
cols = st.columns(2)
for i, eq in enumerate(example_questions):
    if cols[i % 2].button(eq, use_container_width=True):
        st.session_state.question_input = eq
 
st.markdown("---")
 
#Question input
question = st.text_input(
    "Ask a question:",
    value=st.session_state.question_input,
    placeholder="e.g. Which genre has the highest average rating?"
)
 
#Run the pipeline
if question:
    with st.spinner("Translating your question into SQL..."):
        sql_query = question_to_sql(question)
 
    st.subheader("Generated SQL")
    st.code(sql_query, language="sql")
 
    with st.spinner("Running the query against the book database..."):
        columns, rows = execute_query(sql_query)
 
    with st.spinner("Writing your answer..."):
        answer = phrase_answer(question, columns, rows)
 
    st.subheader("Answer")
    st.success(answer)
 
#Dataset description + preview (shown below the question section)
st.markdown('<div class="section-header"></div>', unsafe_allow_html=True)
st.subheader("About this dataset")
st.markdown("""
This assistant is built on the **Goodbooks-10k** dataset — roughly 10,000 books and millions of reader ratings, originally sourced from Goodreads.
 
**Tables behind this project:**
- `dim_books` — one row per book (title, genres, authors, rating, popularity bucket)
- `book_authors` — one row per (book, author) pair, since a book can have multiple authors
- `fact_ratings` — one row per individual reader rating (1–5 stars)
 
The raw data was cleaned and loaded through a PySpark/Delta Lake pipeline on Databricks, then modeled into a simple star schema before being made queryable through this assistant.""")
 
with st.spinner("Loading a preview of the data..."):
    try:
        columns, rows = get_table_preview("dim_books", limit=5)
        st.dataframe(
            {col: [row[i] for row in rows] for i, col in enumerate(columns)},
            use_container_width=True
        )
    except Exception as e:
        st.caption(f"Preview unavailable right now: {e}")
 
#Footer
st.markdown(
    '<p class="footer-note">Simplified portfolio project: Databricks Volumes → '
    'Databricks (PySpark, Delta Lake) → star-schema data model → Claude API for '
    'natural-language-to-SQL. Only SELECT queries are permitted; all generated '
    'SQL is validated before execution.</p>',
    unsafe_allow_html=True
)