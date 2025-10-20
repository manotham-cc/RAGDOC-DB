"""This module generates a user-friendly summary of a SQL query result."""

from ragsql.utils.load_prompt_txt import load_prompt_template
from ragsql.execute_query import execute_sql_query
from ragsql.llm import get_llm_response
from ragsql.history import get_chat_history

def get_summary(session_id: str, user_question: str) -> tuple[str, str]:
    """
    Generates a user-friendly summary of a SQL query result.

    Args:
        session_id: The ID of the current chat session.
        user_question: The user's original natural language question.

    Returns:
        A tuple containing the summary and the generated SQL query.
    """
    summary_prompt_template = load_prompt_template("prompt_templates/summary_prompt.txt")
    results, sql_query = execute_sql_query(session_id, user_question)

    # Retrieve and format the chat history
    history = get_chat_history(session_id)
    formatted_history = "\n".join([f"User: {q}\nAI: {a}" for q, a in history])

    final_prompt = summary_prompt_template.format(
        user_question=user_question,
        sql_query=sql_query,
        results=results,
        chat_history=formatted_history
    )

    response = get_llm_response(final_prompt, user_question)
    return response, sql_query

# Example usage
if __name__ == "__main__":  
    user_question = "List all high-severity cybersecurity incidents"
    print("==================================================")
    response = get_summary(user_question)
    print(response)