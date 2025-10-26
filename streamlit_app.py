import streamlit as st
import uuid
from utils.intent import classify_intent
from ragsql.sql_rag_summary import get_sql_rag
from ragdoc.doc_rag_summary import get_doc_rag
from ragsql.history import save_chat_history, get_chat_history

st.set_page_config(page_title="Ongkhot Chatbot", page_icon=":robot:")
st.title("Ongkhot Chatbot")
st.write("AI-powered cybersecurity incident analysis assistant.")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    history = get_chat_history(st.session_state.session_id, limit=10)
    for q, a in history:
        st.session_state.messages.append({"role": "user", "content": q})
        st.session_state.messages.append({"role": "assistant", "content": a})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Your question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                intent = classify_intent(prompt)
                st.write(f"Intent: {intent}")

                if intent == "sql":
                    ai_summary, sql_query = get_sql_rag(st.session_state.session_id, prompt)
                    st.markdown(ai_summary)
                    with st.expander("Generated SQL Query"):
                        st.code(sql_query, language="sql")
                    save_chat_history(st.session_state.session_id, prompt, sql_query, ai_summary)
                    st.session_state.messages.append({"role": "assistant", "content": ai_summary})

                elif intent == "doc":
                    ai_summary, context = get_doc_rag(st.session_state.session_id, prompt)
                    st.markdown(ai_summary)
                    with st.expander("Document References"):
                        st.text(context)
                    save_chat_history(st.session_state.session_id, prompt, context, ai_summary)
                    st.session_state.messages.append({"role": "assistant", "content": ai_summary})

                else:
                    st.error("Could not determine the intent of the question. Please try again.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
