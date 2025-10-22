"""This module provides a reusable function for interacting with the language model."""

from ragsql.config import client

def get_llm_response(system_prompt: str, user_message: str) -> str:
    """
    Sends a request to the language model and returns the response.

    Args:
        system_prompt: The system prompt to send to the model.
        user_message: The user message to send to the model.

    Returns:
        The content of the model's response.
    """
    completion = client.chat.completions.create(
        extra_body={},
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    return completion.choices[0].message.content
