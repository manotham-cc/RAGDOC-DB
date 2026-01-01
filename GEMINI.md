# Ongkhot Chatbot (Multi-Source RAG)

**Project Type:** Python Application (CLI & Streamlit)

## Project Overview

Ongkhot Chatbot is an AI-powered cybersecurity incident analysis assistant. It utilizes a Multi-Source Retrieval-Augmented Generation (RAG) architecture to answer user queries by retrieving information from two distinct sources:
1.  **SQL Database:** Structured data queried via generated SQL.
2.  **Documents:** Unstructured text (e.g., security guides) retrieved via vector similarity search.

The system uses an intent classification step to route queries to the appropriate handler (`doc` or `sql`).

## Architecture

*   **Frontend:**
    *   `streamlit_app.py`: Web interface powered by Streamlit.
    *   `main.py`: Interactive Command Line Interface.
*   **Core Logic:**
    *   `utils/intent.py`: Classifies user queries into `sql` or `doc` intents.
    *   `ragsql/`: Handles SQL generation, execution, and summarization.
    *   `ragdoc/`: Handles document embedding, retrieval, and summarization.
*   **Data Storage:**
    *   **PostgreSQL**: Used for structured data, chat history, and vector storage (`pgvector`).
    *   **Vectors**: Embeddings generated using `sentence-transformers` (`intfloat/multilingual-e5-large-instruct`).

## Setup & Installation

### 1. Prerequisites
*   Python 3.10+ (Check `.python-version` if available)
*   Docker & Docker Compose (for database services)

### 2. Environment Variables
Create a `.env` file in the root directory. Based on `ragsql/config.py`, you need the following:

```env
# AI Provider
OPENROUTER_API_KEY=your_api_key_here

# Main Database
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_PORT=...

# Chat History Database
CHAT_HISTORY_NAME=...
CHAT_HISTORY_USER=...
CHAT_HISTORY_PASSWORD=...
CHAT_HISTORY_HOST=...
CHAT_HISTORY_PORT=...

# Vector Database (pgvector)
VECTOR_NAME=...
VECTOR_USER=...
VECTOR_PASSWORD=...
VECTOR_HOST=...
VECTOR_PORT=...
```

### 3. Installation
```bash
# Create and activate virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirement.txt
```

## Running the Application

### Start Databases
Ensure your PostgreSQL databases are running. A `docker-compose.yml` is present in the root:
```bash
docker-compose up -d
```

### Data Ingestion & Initialization
The system requires both the structured database and the vector index to be populated before use.
*   **Run Initialization Script**:
    This script initializes the main SQL database with sample data and builds the vector index from `security_incident_guide.md`.
    ```bash
    python init_system.py
    ```

### Run CLI
```bash
python main.py
```

### Run Web Interface
```bash
streamlit run streamlit_app.py
```

## Project Structure Key
*   `handlers/`: Bridges the intent classification to the specific RAG implementation.
*   `prompt_templates/`: Text files containing prompts for the LLM (SQL generation, RAG summarization, etc.).
*   `tests/`: Integration and unit tests. Run with `pytest`.
*   `init-history-db.sql`: SQL script to initialize the chat history schema.

## Development Notes
*   **Embeddings**: The project uses a local embedding model path. Ensure the model is downloaded or update `ragdoc/build_index.py` to download it automatically if missing.
*   **Database Connections**: There are three distinct connection functions in `ragsql/config.py`. Ensure all three sets of credentials are correct in your `.env`.
