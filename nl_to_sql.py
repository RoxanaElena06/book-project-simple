import os
import anthropic
from schema_context import SCHEMA_CONTEXT

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


#Turn a question into SQL
def question_to_sql(question):
    prompt = f"""Here is a database schema:
{SCHEMA_CONTEXT}

Write ONE SQL SELECT query (nothing else, no explanation) that answers:
{question}
"""
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    sql_query = response.content[0].text.strip()
    return sql_query


#Turn SQL results into a English sentence
def phrase_answer(question, columns, rows):
    results_as_text = f"{columns}\n{rows}"

    prompt = f"""Question: {question}
Query results: {results_as_text}

Answer the question in one short sentence, using only this data.
"""
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


#TRY IT
if __name__ == "__main__":
    from execute_sql import execute_query

    question = "Which genre has the highest average rating?"
    sql = question_to_sql(question)
    print("Generated SQL:", sql)

    columns, rows = execute_query(sql)
    answer = phrase_answer(question, columns, rows)
    print("Answer:", answer)
