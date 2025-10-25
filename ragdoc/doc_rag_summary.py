from sentence_transformers import SentenceTransformer
from ragsql.config import get_chat_vector_db_connection
from ragsql.utils.load_prompt_txt import load_prompt_template
from ragsql.llm import get_llm_response
import os
# ==========================
# CONFIG
# ==========================
home = os.path.expanduser("~")
model_path = os.path.join(
    home,
    ".cache",
    "huggingface",
    "hub",
    "models--intfloat--multilingual-e5-large-instruct",
    "snapshots",
    "274baa43b0e13e37fafa6428dbc7938e62e5c439"
)
model = SentenceTransformer(model_path)

# ==========================
# CONNECT VECTOR DATABASE (pgvector)
# ==========================
conn = get_chat_vector_db_connection()
cur = conn.cursor()

# ==========================
# RETRIEVE (RAG PIPELINE)
# ==========================
def retrieve_relevant_context(query, top_k=3):
    q_emb = model.encode([query], normalize_embeddings=True)[0]
    cur.execute(
        "SELECT content FROM documents ORDER BY embedding <-> %s::vector LIMIT %s;",
        (q_emb.tolist(), top_k)
    )

    return [r[0] for r in cur.fetchall()]

# ==========================
# GENERATE ANSWER (LLM CALL)
# ==========================
def generate_answer(query):
    context = retrieve_relevant_context(query)
    prompt = load_prompt_template("prompt_templates/doc_rag_prompt.txt")
    final_prompt = prompt.format(
        user_question=query,
        Context_Retrieved="\n---\n".join(context)
    )
    respone = get_llm_response(final_prompt, query)
    return respone 

# ==========================
# TEST
# ==========================
if __name__ == "__main__":
    query = "How to prevent SQL breach?"
    answer = generate_answer(query)
    print("\n=== ANSWER ===\n")
    print(answer)

    cur.close()
    conn.close()