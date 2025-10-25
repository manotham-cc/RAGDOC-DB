"""This module handles the configuration for the database and the OpenAI API client."""

import os
from dotenv import load_dotenv
from openai import OpenAI
import psycopg2

load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

def get_db_connection():
  """
  Establishes a connection to the PostgreSQL database.

  Returns:
      A psycopg2 connection object or None if the connection fails.
  """
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

def get_chat_history_db_connection():
  """
  Establishes a connection to the chat history PostgreSQL database.

  Returns:
      A psycopg2 connection object or None if the connection fails.
  """
  try:
    conn = psycopg2.connect(
      dbname=os.getenv("POSTGRES_DB_CHAT"),
      user=os.getenv("POSTGRES_USER_CHAT"),
      password=os.getenv("POSTGRES_PASSWORD_CHAT"),
      host=os.getenv("POSTGRES_HOST_CHAT"),
      port=os.getenv("POSTGRES_PORT_CHAT"),
    )
    return conn
  except psycopg2.Error as e:
    print(f"Error connecting to the chat history database: {e}")
    return None
def get_chat_vector_db_connection():
  """
  Establishes a connection to the vector_db knowledge PostgreSQL database.

  Returns:
      A psycopg2 connection object or None if the connection fails.
  """
  try:
    conn = psycopg2.connect(
      dbname=os.getenv("POSTGRES_DB_VECTOR"),
      user=os.getenv("POSTGRES_USER_VECTOR"),
      password=os.getenv("POSTGRES_PASSWORD_VECTOR"),
      host=os.getenv("POSTGRES_HOST_VECTOR"),
      port=os.getenv("POSTGRES_PORT_VECTOR"),
    )
    return conn
  except psycopg2.Error as e:
    print(f"Error connecting to the chat history database: {e}")
    return None