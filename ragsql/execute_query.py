"""This module executes a SQL query against the database."""

import logging
from core.config import get_db_connection
from ragsql.nlq_parser import question_to_sql

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def execute_sql_query(session_id: str, user_question: str) -> tuple[list, str]:
    """
    Executes a SQL query generated from a natural language question.

    Args:
        session_id: The ID of the current chat session.
        user_question: The natural language question.

    Returns:
        A tuple containing the query results and the generated SQL query.
    """
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            logger.error("Database connection failed.")
            return "Database connection failed.", ""

        cursor = conn.cursor()
        sql_query = question_to_sql(session_id, user_question)
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results, sql_query
    except Exception as e:
        logger.error(f"Error executing NLQ query: {e}")
        return f"Error executing NLQ query: {e}", ""
    finally:
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    user_question = "List all high-severity cybersecurity incidents"
    # Note: passing dummy session_id for test
    results = execute_sql_query("test_session", user_question)
    print(results)