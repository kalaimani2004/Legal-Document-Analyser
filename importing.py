import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect("postgresql://postgres:postgre@localhost:5432/legal_docs_analyser")
cursor = conn.cursor()

with open('legal_terms.csv', 'r', encoding='utf-8') as f:
    next(f)  # Skip the header row
    cursor.copy_expert("COPY legal_terms(term, simplified_term) FROM STDIN WITH CSV HEADER", f)

conn.commit()
cursor.close()
conn.close()
