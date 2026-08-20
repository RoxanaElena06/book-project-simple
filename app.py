import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from nl_to_sql import question_to_sql, phrase_answer
from execute_sql import execute_query

st.title("📚 Book Data Assistant (simplified)")

question = st.text_input("Ask a question about the book data:")

if question:
    sql_query = question_to_sql(question)
    st.code(sql_query, language="sql")

    columns, rows = execute_query(sql_query)
    answer = phrase_answer(question, columns, rows)

    st.write(answer)
