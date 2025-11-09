from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import sqlite3
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_output_tokens=None,
    timeout=None,
    max_retries=2,
)

# Prompt definition
prompt = """
You are an expert in converting English questions to SQL queries!
The SQL database has a table named students and has the following columns:
ID, NAME, CLASS, SECTION, MARKS.
The SQL database has a table named teachers and has the following columns:
ID, NAME, SUBJECT.

Examples:
Q: How many records are present?
A: SELECT COUNT(*) FROM students;

Q: Tell me all the students studying in Data Science class.
A: SELECT * FROM STUDENT WHERE CLASS="Data Science";

Return only the SQL query, no explanation, no ```sql``` block.
"""

# Function to get Gemini response
def get_gemini_response(question, prompt):
    response = llm.invoke(prompt + "\n\nQuestion: " + question)
    return response.content.strip()  # Use .content not .text (for newer LangChain versions)

# Function to run SQL query
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        return f"Error executing SQL: {e}"
    finally:
        conn.close()

# Streamlit app
st.set_page_config(page_title="SQL Query Generator")
st.header("🧠 Gemini App to Retrieve SQL Data")

question = st.text_input("Enter your question:", key="input")

if st.button("Ask"):
    sql_query = get_gemini_response(question, prompt)
    st.subheader("Generated SQL Query")
    st.code(sql_query, language="sql")

    result = read_sql_query(sql_query, "student.db")

    st.subheader("Query Result")
    if isinstance(result, str):
        st.error(result)
    elif len(result) > 0:
        for row in result:
            st.write(row)
    else:
        st.info("No results found.")
