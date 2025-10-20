"""This module converts a natural language question to a SQL query."""

from ragsql.schema_loader import get_database_schema, format_schema
from ragsql.utils.load_prompt_txt import load_prompt_template
from ragsql.llm import get_llm_response
from ragsql.history import get_chat_history

def question_to_sql(session_id: str, user_question: str) -> str:
    """
    Converts a natural language question to a SQL query using the LLM,
    with the context of the chat history.
    """
    schema = get_database_schema()
    formatted_schema = format_schema(schema)
    prompt_template = load_prompt_template("prompt_templates/nl2sql_prompt.txt")

    # Retrieve and format the chat history
    history = get_chat_history(session_id)
    formatted_history = "\n".join([f"User: {q}\nAI: {a}" for q, a in history])

    final_prompt = prompt_template.format(
        formatted_schema=formatted_schema,
        chat_history=formatted_history
    )

    sql_query = get_llm_response(final_prompt, user_question)
    return sql_query

if __name__ == "__main__":
    # Example usage
    question = "List all high-severity cybersecurity incidents"
    print(question_to_sql(question))
