from ragsql.config import client
from ragsql.utils.load_prompt_txt import load_prompt_template
from ragsql.execute_query import execute_sql_query

def get_summary(user_question: str) -> str:
    summary_prompt = load_prompt_template("prompt_templates/summary_prompt.txt")
    results , sql_query = execute_sql_query(user_question)
    final_prompt = summary_prompt.format(user_question=user_question, sql_query=sql_query ,results=results)
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
    response = completion.choices[0].message.content
    return response , sql_query

# Example usage
if __name__ == "__main__":  
    user_question = "List all high-severity cybersecurity incidents"
    print("==================================================")
    response = get_summary(user_question)
    print(response)