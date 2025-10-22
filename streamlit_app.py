import streamlit as st
import uuid
from ragsql.summary import get_summary
from ragsql.history import save_chat_history, get_chat_history

st.set_page_config(page_title="Ongkhot Chatbot", page_icon=":robot:")
st.title("Ongkhot Chatbot")
st.write("AI-powered cybersecurity incident analysis assistant.")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    # Load existing chat history for this session if available
    st.session_state.messages = []
    history = get_chat_history(st.session_state.session_id, limit=10) # Load last 10 messages
    for q, a in history:
        st.session_state.messages.append({"role": "user", "content": q})
        st.session_state.messages.append({"role": "assistant", "content": a})

# Display chat messages from history on app rerun
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
                ai_summary, sql_query = get_summary(st.session_state.session_id, prompt)
                st.markdown(ai_summary)
                with st.expander("Generated SQL Query"):
                    st.code(sql_query, language="sql")

                # Save chat history
                save_chat_history(st.session_state.session_id, prompt, sql_query, ai_summary)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                ai_summary = f"Error: {e}"
                sql_query = ""

        st.session_state.messages.append({"role": "assistant", "content": ai_summary})
