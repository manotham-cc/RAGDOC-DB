import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

# --- Postgres DB connection setup ---
import psycopg2

def get_db_connection():
  try:
    conn = psycopg2.connect(
      dbname=os.getenv("POSTGRES_DB"),
      user=os.getenv("POSTGRES_USER"),
      password=os.getenv("POSTGRES_PASSWORD"),
      host=os.getenv("POSTGRES_HOST"),
      port=os.getenv("POSTGRES_PORT"),
    )
    return conn
  except psycopg2.Error as e:
    print(f"Error connecting to the database: {e}")
    return None