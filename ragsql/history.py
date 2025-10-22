# ragsql/history.py
"""This module handles saving and retrieving chat history from the database."""

from ragsql.config import get_chat_history_db_connection

def save_chat_history(session_id: str, user_question: str, sql_query: str, ai_summary: str):
    """Saves a chat interaction to the database."""
    conn = get_chat_history_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chat_history (session_id, user_question, sql_query, ai_summary)
                VALUES (%s, %s, %s, %s)
                """,
                (session_id, user_question, sql_query, ai_summary),
            )
            conn.commit()
    except Exception as e:
        print(f"Error saving chat history: {e}")
    finally:
        if conn:
            conn.close()

def get_chat_history(session_id: str, limit: int = 5) -> list[tuple[str, str]]:
    """Retrieves the recent chat history for a session."""
    conn = get_chat_history_db_connection()
    if conn is None:
        return []

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT user_question, ai_summary
                FROM chat_history
                WHERE session_id = %s
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (session_id, limit),
            )
            history = cur.fetchall()
            # Reverse the history to be in chronological order
            return list(reversed(history))
    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        return []
    finally:
        if conn:
            conn.close()
