from sentence_transformers import SentenceTransformer
from core.config import get_chat_vector_db_connection, get_model_path
from utils.load_prompt_txt import load_prompt_template
from core.llm import get_llm_response
from core.history import get_chat_history
import logging

# ========================== 
# CONFIG & LOGGING
# ========================== 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model_path = get_model_path()
try:
    model = SentenceTransformer(model_path)
except Exception as e:
    logger.error(f"Failed to load model from {model_path}: {e}")
    raise e

# ========================== 
# RETRIEVE (RAG PIPELINE)
# ========================== 
def retrieve_relevant_context(query, top_k=3):
    conn = get_chat_vector_db_connection()
    if not conn:
        logger.error("Could not connect to vector DB")
        return []

    try:
        with conn.cursor() as cur:
            q_emb = model.encode([query], normalize_embeddings=True)[0]
            cur.execute(
                "SELECT content FROM documents ORDER BY embedding <-> %s::vector LIMIT %s;",
                (q_emb.tolist(), top_k)
            )
            return [r[0] for r in cur.fetchall()]
    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        return []
    finally:
        if conn:
            conn.close()

# ========================== 
# GENERATE ANSWER (LLM CALL)
# ========================== 
def get_doc_rag(session_id, user_question):
    context = retrieve_relevant_context(user_question)
    prompt = load_prompt_template("prompt_templates/doc_rag_prompt.txt")
    history = get_chat_history(session_id)
    formatted_history = "\n".join([f"User: {q}\nAI: {a}" for q, a in history])
    final_prompt = prompt.format(
        user_question=user_question,
        Context_Retrieved="\n---\n".join(context),
        chat_history=formatted_history
    )

    response = get_llm_response(final_prompt, user_question)
    return response, context

# ========================== 
# TEST
# ========================== 
if __name__ == "__main__":
    # Note: This test block might fail if run directly without a valid DB connection
    user_question = "How to prevent SQL breach?"
    try:
        answer, ctx = get_doc_rag("test_session", user_question)
        print("\n=== ANSWER ===\n")
        print(answer)
    except Exception as e:
        print(f"Test failed: {e}")
