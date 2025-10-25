import os
import psycopg2
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer
from ragsql.config import get_chat_vector_db_connection
from ragsql.llm import get_llm_response

# ==========================
# CONFIG
# ==========================
home = os.path.expanduser("~")
model_path = os.path.join(
    home,
    ".cache",
    "huggingface",
    "hub",
    "models--intfloat--multilingual-e5-large-instruct",
    "snapshots",
    "274baa43b0e13e37fafa6428dbc7938e62e5c439"
)
doc_path = os.path.join(home, "Desktop", "RAGDOC-DB", "security_incident_guide.md")

# ==========================
# LOAD MODEL
# ==========================
model = SentenceTransformer(model_path)

# ==========================
# CONNECT VECTOR DATABASE (pgvector)
# ==========================
conn = get_chat_vector_db_connection()
cur = conn.cursor()

# ==========================
# CREATE TABLE IF NOT EXISTS
# ==========================
cur.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1024)
);
""")
conn.commit()

# ==========================
# LOAD AND ENCODE DOCUMENT
# ==========================
with open(doc_path, "r", encoding="utf-8") as f:
    text = f.read()

chunks = [t.strip() for t in text.split("\n\n") if t.strip()]
vectors = model.encode(chunks, normalize_embeddings=True)

# ==========================
# INSERT INTO DATABASE
# ==========================
records = list(zip(chunks, [v.tolist() for v in vectors]))
execute_values(
    cur,
    "INSERT INTO documents (content, embedding) VALUES %s",
    records
)
conn.commit()
print(f"Inserted {len(records)} chunks.")
cur.close()
conn.close()
