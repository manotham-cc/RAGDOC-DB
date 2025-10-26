import uuid
from utils.intent import classify_intent
from handlers.doc_handler import handle_doc_rag
from handlers.sql_handler import handle_sql_rag

def main() -> None:
    session_id = str(uuid.uuid4())
    print(f"Starting new chat session: {session_id}")

    while True:
        try:
            question = input("\nEnter your question (or 'exit' to end): ").strip()
            if question.lower() == "exit":
                break
            if not question:
                continue

            intent = classify_intent(question)
            print(f"Identified intent: {intent}")

            if intent == "doc":
                handle_doc_rag(session_id, question)
            elif intent == "sql":
                handle_sql_rag(session_id, question)
            else:
                print("Unrecognized intent. Please ask again.")

        except (EOFError, KeyboardInterrupt):
            print("\nInterrupted by user.")
            break
        except Exception as e:
            print(f"Error: {e}")

    print("\nChat session ended.")


if __name__ == "__main__":
    main()
