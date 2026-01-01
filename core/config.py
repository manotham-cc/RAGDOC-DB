"""This module handles the configuration for the database and the OpenAI API client."""

import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
import psycopg2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize OpenAI Client
try:
    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=os.getenv("OPENROUTER_API_KEY"),
    )
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None

def _create_connection(dbname_key, user_key, password_key, host_key, port_key, default_host="localhost"):
    """
    Helper function to establish a database connection using environment variables.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv(dbname_key),
            user=os.getenv(user_key),
            password=os.getenv(password_key),
            host=os.getenv(host_key, default_host),
            port=os.getenv(port_key),
        )
        return conn
    except psycopg2.Error as e:
        # Log the error but mask credentials if possible (keys are passed, not values, so it's safe)
        logger.error(f"Error connecting to database (Config Keys: {dbname_key}): {e}")
        return None

def get_db_connection():
    """Establishes a connection to the main PostgreSQL database."""
    return _create_connection("DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT")

def get_chat_history_db_connection():
    """Establishes a connection to the chat history PostgreSQL database."""
    return _create_connection("CHAT_HISTORY_NAME", "CHAT_HISTORY_USER", "CHAT_HISTORY_PASSWORD", "CHAT_HISTORY_HOST", "CHAT_HISTORY_PORT")

def get_chat_vector_db_connection():
    """Establishes a connection to the vector knowledge PostgreSQL database."""
    return _create_connection("VECTOR_NAME", "VECTOR_USER", "VECTOR_PASSWORD", "VECTOR_HOST", "VECTOR_PORT")

def get_model_path():
    """Returns the local path to the embedding model."""
    env_path = os.getenv("EMBEDDING_MODEL_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
    elif env_path:
        logger.warning(f"EMBEDDING_MODEL_PATH set to '{env_path}' but path does not exist. Falling back to default.")
    
    # Default fallback
    home = os.path.expanduser("~")
    # Determine the separator based on OS, though os.path.join handles it.
    # We keep the original logic for backward compatibility
    return os.path.join(
        home,
        ".cache",
        "huggingface",
        "hub",
        "models--intfloat--multilingual-e5-large-instruct",
        "snapshots",
        "274baa43b0e13e37fafa6428dbc7938e62e5c439"
    )

def get_doc_path():
    """Returns the path to the source document."""
    path = os.getenv("DOC_PATH")
    if path:
        return path

    # Default fallback
    home = os.path.expanduser("~")
    return os.path.join(home, "Desktop", "Multi-Source-RAG", "security_incident_guide.md")
