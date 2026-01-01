from ragdoc.doc_rag_summary import get_doc_rag
from core.history import save_chat_history

def handle_doc_rag(session_id: str, question: str) -> None:
    response, context = get_doc_rag(session_id,question)
    print("\n--- USER-FACING SUMMARY ---\n", response)
    print("\n--- DOCUMENTS REF ---\n",context )
    save_chat_history(session_id, question, context, response)
