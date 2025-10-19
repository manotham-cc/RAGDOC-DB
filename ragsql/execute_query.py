from ragsql.config import get_db_connection
from ragsql.nlq_parser import question_to_sql

def execute_sql_query(user_question: str):
    """
    Executes an NLQ query by first converting it to SQL using the LLM,
    then executing the SQL against the database and returning the results.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql_query = question_to_sql(user_question)
        print("Generated SQL Query:", sql_query)
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results , sql_query
    except Exception as e:
        print(f"Error executing NLQ query: {e}")
        return  (f"Error executing NLQ query: {e}")
    finally:
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    user_question = "List all high-severity cybersecurity incidents"
    results = execute_sql_query(user_question)
    print(results)
