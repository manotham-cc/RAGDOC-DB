import os
import logging
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer
from core.config import get_chat_vector_db_connection, get_model_path, get_doc_path

# ========================== 
# CONFIG & LOGGING
# ========================== 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def build_vector_index():
    """
    Connects to the vector database, creates the documents table if it doesn't exist,
    loads the document, generates embeddings, and inserts them into the database.
    """
    model_path = get_model_path()
    doc_path = get_doc_path()

    logger.info(f"Using model path: {model_path}")
    logger.info(f"Using document path: {doc_path}")

    # ========================== 
    # LOAD MODEL
    # ========================== 
    try:
        model = SentenceTransformer(model_path)
    except Exception as e:
        logger.error(f"Failed to load model from {model_path}. Ensure the path is correct or the model is downloaded. Error: {e}")
        return

    # ========================== 
    # CONNECT VECTOR DATABASE (pgvector)
    # ========================== 
    conn = get_chat_vector_db_connection()
    if not conn:
        logger.error("Failed to connect to vector database. Exiting.")
        return

    cur = conn.cursor()

    # ========================== 
    # CREATE TABLE IF NOT EXISTS
    # ========================== 
    try:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            content TEXT,
            embedding vector(1024)
        );
        """
        )
        conn.commit()
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        conn.close()
        return

    # ========================== 
    # LOAD AND ENCODE DOCUMENT
    # ========================== 
    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = [t.strip() for t in text.split("\n\n") if t.strip()]
        
        if not chunks:
            logger.warning("No content found in document to index.")
        else:
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
            logger.info(f"Successfully inserted {len(records)} chunks.")
            
    except FileNotFoundError:
        logger.error(f"Document not found at {doc_path}")
    except Exception as e:
        logger.error(f"An error occurred during indexing: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    build_vector_index()
