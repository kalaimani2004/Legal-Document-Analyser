import re
import psycopg2
from transformers import pipeline
from dotenv import load_dotenv
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # suppress TensorFlow INFO and WARNING messages


load_dotenv()

# Load summarization model only once
print("Loading model...")  # Good for GMeet presentation
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
print("Model loaded successfully!")

# Get DB connection string
db_uri = os.getenv("POSTGRES_URI")

# Fetch legal terms from DB
def get_legal_terms():
    try:
        with psycopg2.connect(db_uri) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT term, simplified_term FROM legal_terms")
                return cursor.fetchall()
    except Exception as e:
        print("Error fetching legal terms:", e)
        return []

# Replace legal terms with simplified explanations
def explain_terms(text):
    legal_terms = get_legal_terms()
    for term, simplified in legal_terms:
        pattern = rf"\b{re.escape(term)}\b"
        text = re.sub(pattern, f"{term} ({simplified})", text, flags=re.IGNORECASE)
    return text

# Fetch relevant laws from DB
def fetch_relevant_laws(text):
    try:
        with psycopg2.connect(db_uri) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT section, description FROM laws")
                all_laws = cursor.fetchall()
    except Exception as e:
        print("Error fetching laws:", e)
        return []

    matched_laws = []
    for section, description in all_laws:
        if re.search(rf'\b{section}\b', text, re.IGNORECASE) or re.search(rf'\b{description.split()[0]}\b', text, re.IGNORECASE):
            matched_laws.append((section, description))
    return matched_laws

# Break document into chunks
def chunk_text(text, max_tokens=1000):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current_chunk = [], ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_tokens:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# Paragraph formatting for clean output
def format_summary_text(summary_text, sentences_per_paragraph=2):
    sentences = re.split(r'(?<=[.!?]) +', summary_text.strip())
    paragraphs = [" ".join(sentences[i:i+sentences_per_paragraph]) for i in range(0, len(sentences), sentences_per_paragraph)]
    return "\n\n".join(paragraphs)

#  Main function
def summarize_document(document):
    try:
        print("Summarizing document...")  # Helpful for demo
        chunks = chunk_text(document)
        summarized_chunks = []

        for chunk in chunks:
            summary = summarizer(chunk, max_length=100, min_length=50, do_sample=False)[0]['summary_text']
            summarized_chunks.append(summary)

        full_summary = " ".join(summarized_chunks)
        formatted_summary = format_summary_text(full_summary)
        explained_summary = explain_terms(formatted_summary)

        laws = fetch_relevant_laws(document)
        if laws:
            law_text = "\n\nRelated Legal Sections:\n" + "\n".join([f"{s} - {d}" for s, d in laws])
        else:
            law_text = "\n\nNo specific legal references found."

        print("Summarization complete!")
        return explained_summary + law_text

    except Exception as e:
        print("Error during summarization:", e)
        return "An error occurred while processing the document. Please try again later."

