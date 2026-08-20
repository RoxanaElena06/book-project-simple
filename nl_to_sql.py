import os
import anthropic
from schema_context import SCHEMA_CONTEXT

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def extract_text(response):
    text_blocks = [block.text for block in response.content if block.type == "text"]
    return "".join(text_blocks).strip()

def clean_sql(raw_sql):
    cleaned = raw_sql.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
        cleaned = cleaned.lstrip("sql").lstrip()
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    return cleaned.strip()

#Turn a question into SQL
def question_to_sql(question):
    prompt = f"""Here is a database schema:
{SCHEMA_CONTEXT}

This database runs on Databricks (Spark SQL). For array columns like
'genres' or working with book_authors, use LATERAL VIEW explode(...),
NOT UNNEST(...) -- UNNEST is not supported in this SQL dialect.

Write ONE SQL SELECT query (nothing else, no explanation) that answers:
{question}
"""
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    raw_output = extract_text(response)
    return clean_sql(raw_output)


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
    return extract_text(response)


#TRY IT
if __name__ == "__main__":
    from execute_sql import execute_query

    question = "Which genre has the highest average rating?"
    sql = question_to_sql(question)
    print("Generated SQL:", sql)

    columns, rows = execute_query(sql)
    answer = phrase_answer(question, columns, rows)
    print("Answer:", answer)
