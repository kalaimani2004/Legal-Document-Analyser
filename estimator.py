import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def estimate_cost(case_type, court_level):
    conn = psycopg2.connect(os.getenv("POSTGRES_URI"))
    cursor = conn.cursor()
    cursor.execute("""
        SELECT average_cost FROM consultation_costs
        WHERE case_type = %s AND court_level = %s
    """, (case_type, court_level))
    row = cursor.fetchone()
    conn.close()

    if row:
        return f"Estimated legal consultation cost: ₹{row[0]}"
    else:
        return "No data available for the selected parameters."

  