from ragsql.config import client
from ragsql.schema_loader import get_database_schema, format_schema
from ragsql.utils.load_prompt_txt import load_prompt_template

def question_to_sql(user_question: str) -> str:
    """
    Runs an NLQ query against the LLM using the database schema and prompt template.
    Returns the LLM response as a string.
    """
    schema = get_database_schema()
    formatted_schema = format_schema(schema)
    prompt_template = load_prompt_template("prompt_templates/nl2sql_prompt.txt")
    final_prompt = prompt_template.format(formatted_schema = formatted_schema)
    completion = client.chat.completions.create(
        extra_body={},
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "system",
                "content": final_prompt
            },
            {
                "role": "user",
                "content": user_question
            }
        ]
    )
    sql_query = completion.choices[0].message.content
    return sql_query

if __name__ == "__main__":
    # Example usage
    question = "List all high-severity cybersecurity incidents"
    print(question_to_sql(question))
