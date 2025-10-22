"""This module executes a SQL query against the database."""

from ragsql.config import get_db_connection
from ragsql.nlq_parser import question_to_sql

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
        cursor = conn.cursor()
        sql_query = question_to_sql(session_id, user_question)
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results, sql_query
    except Exception as e:
        print(f"Error executing NLQ query: {e}")
        return f"Error executing NLQ query: {e}", ""
    finally:
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    user_question = "List all high-severity cybersecurity incidents"
    results = execute_sql_query(user_question)
    print(results)
