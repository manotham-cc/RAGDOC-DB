from ragsql.sql_rag_summary import get_sql_rag
from ragsql.history import save_chat_history

def handle_sql_rag(session_id: str, question: str) -> None:
    response, sql_query = get_sql_rag(session_id,question)
    print("\n--- USER-FACING SUMMARY ---\n", response)
    print("\n--- GENERATED SQL ---\n", sql_query)
    save_chat_history(session_id, question, sql_query, response)
