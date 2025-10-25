# Project Overview

This project is a Python-based application that uses a Retrieval-Augmented Generation (RAG) approach to convert natural language questions into SQL queries. It provides both a command-line interface (CLI) and a web-based chatbot interface using Streamlit.

The application is designed to answer questions about a database of cybersecurity incidents. It takes a user's question in natural language, uses a Large Language Model (LLM) to generate a corresponding SQL query, executes the query against a PostgreSQL database, and then provides a user-friendly summary of the results.

## Key Technologies

*   **Backend:** Python
*   **Frontend (Web):** Streamlit
*   **Database:** PostgreSQL with pgvector for similarity search
*   **LLM Integration:** OpenAI API (via OpenRouter)
*   **Embeddings:** Sentence-Transformers
*   **Core Libraries:**
    *   `psycopg2-binary`: PostgreSQL adapter for Python
    *   `pgvector`: Vector similarity search in PostgreSQL
    *   `sentence-transformers`, `transformers`, `torch`: For creating embeddings
    *   `openai`: OpenAI API client
    *   `streamlit`: For the web-based UI
    *   `python-dotenv`: For managing environment variables

## Architecture

The application is structured into three main parts:

1.  **`ragsql`:** This is the core logic for the natural language to SQL functionality. It contains modules for:
    *   **Configuration (`config.py`):** Manages database connections and API keys.
    *   **Database Schema Loading (`schema_loader.py`):** Retrieves the database schema and formats it for the LLM.
    *   **LLM Interaction (`llm.py`):** Handles communication with the LLM.
    *   **Natural Language to SQL (`nlq_parser.py`):** Parses the user's question and, with the help of the LLM, generates a SQL query.
    *   **Query Execution (`execute_query.py`):** Executes the generated SQL query.
    *   **Summarization (`summary.py`):** Generates a user-friendly summary of the query results.
    *   **Chat History (`history.py`):** Saves and retrieves chat history.

2.  **`ragdoc`:** This directory contains the logic for the document-based Retrieval-Augmented Generation (RAG) functionality. It is used for answering questions based on a document.
    *   **`build_index.py`:** This script reads a document, splits it into chunks, generates embeddings for each chunk, and stores them in a vector database.
    *   **`retriveval.py`:** This script takes a user's query, retrieves relevant document chunks from the vector database, and uses an LLM to generate an answer.

3.  **Interfaces:**
    *   **`main.py`:** A command-line interface (CLI) for interacting with the `ragsql` functionality.
    *   **`streamlit_app.py`:** A web-based chatbot interface built with Streamlit that uses the `ragsql` functionality.

## Building and Running

### Prerequisites

*   Python 3.x
*   PostgreSQL database
*   An OpenAI API key (or an API key for a compatible service like OpenRouter)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up the environment variables:**
    Create a `.env` file in the root of the project and add the following variables:
    ```
    OPENROUTER_API_KEY=<your-openrouter-api-key>
    POSTGRES_DB=<your-database-name>
    POSTGRES_USER=<your-database-user>
    POSTGRES_PASSWORD=<your-database-password>
    POSTGRES_HOST=<your-database-host>
    POSTGRES_PORT=<your-database-port>
    POSTGRES_DB_CHAT=<your-chat-history-database-name>
    POSTGRES_USER_CHAT=<your-chat-history-database-user>
    POSTGRES_PASSWORD_CHAT=<your-chat-history-database-password>
    POSTGRES_HOST_CHAT=<your-chat-history-database-host>
    POSTGRES_PORT_CHAT=<your-chat-history-database-port>
    POSTGRES_DB_VECTOR=<your-vector-database-name>
    POSTGRES_USER_VECTOR=<your-vector-database-user>
    POSTGRES_PASSWORD_VECTOR=<your-vector-database-password>
    POSTGRES_HOST_VECTOR=<your-vector-database-host>
    POSTGRES_PORT_VECTOR=<your-vector-database-port>
    ```

### Building the Document Index

To use the document-based question answering functionality (`ragdoc`), you first need to build an index of the documents you want to query. You can do this by running the `build_index.py` script:

```bash
python -m ragdoc.build_index
```

This script will read the `security_incident_guide.md` file, generate embeddings for its content, and store them in the vector database.

### Running the Application

*   **Command-Line Interface:**
    ```bash
    python main.py
    ```

*   **Web Interface:**
    ```bash
    streamlit run streamlit_app.py
    ```

## Development Conventions

*   **Code Style:** The code follows standard Python conventions (PEP 8).
*   **Testing:** The project includes a `tests` directory, suggesting that it uses `pytest` for testing. To run the tests, you would typically use the following command:
    ```bash
    pytest
    ```
*   **Modularity:** The code is organized into modules with specific responsibilities, which makes it easier to understand and maintain.
*   **Environment Variables:** The use of `python-dotenv` for managing configuration is a good practice for keeping sensitive information out of the codebase.
