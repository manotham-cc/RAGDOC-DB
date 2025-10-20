"""This module is the main entry point for the RAGSQL application."""

import uuid
from ragsql.summary import get_summary
from ragsql.history import save_chat_history

def main():
    """The main function for the RAGSQL application."""
    session_id = str(uuid.uuid4())
    print(f"Starting new chat session: {session_id}")

    while True:
        try:
            question = input("Enter your natural-language question (or 'exit' to end): ")
            if question.lower() == 'exit':
                break
            if not question:
                continue

            response, sql = get_summary(session_id, question)
            print("\n--- USER-FACING SUMMARY ---\n")
            print(response)
            print("\n--- GENERATED SQL ---\n")
            print(sql)

            # Save the chat history
            save_chat_history(session_id, question, sql, response)

        except (EOFError, KeyboardInterrupt):
            break

    print("\nChat session ended.")

if __name__ == "__main__":
    main()
