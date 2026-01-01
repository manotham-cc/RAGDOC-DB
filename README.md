# Ongkhot Chatbot (Multi-Source RAG)

Ongkhot is an AI-powered cybersecurity incident analysis assistant. It utilizes a **Multi-Source Retrieval-Augmented Generation (RAG)** architecture to provide accurate answers by dynamically routing queries to either structured database data or unstructured documentation.

## 🚀 Features

-   **Multi-Source Retrieval:** Seamlessly switches between SQL databases and document vector stores.
-   **Intent Classification:** Automatically detects if a question requires a database query or a document lookup.
-   **Natural Language to SQL (NL2SQL):** Converts natural language questions into executable SQL queries.
-   **Semantic Search:** Uses `pgvector` and `sentence-transformers` for high-accuracy document retrieval.
-   **Chat History:** Persists conversation history in a PostgreSQL database.
-   **Dual Interface:** Includes both a Command Line Interface (CLI) and a modern Streamlit web UI.
-   **Configurable Architecture:** Easily customize embedding models and document sources via environment variables.

## 🏗️ Architecture

-   **Frontend:** Streamlit (`streamlit_app.py`) & CLI (`main.py`)
-   **Core Logic (`core/`):** Shared configuration, LLM client, and history management.
-   **Orchestration:** Intent classifier (`utils/intent.py`) routes to specific handlers.
-   **Handlers (`handlers/`):** Bridges intent to specific RAG implementations.
-   **SQL RAG (`ragsql/`):** Schema loading, NL2SQL generation, and query execution.
-   **Doc RAG (`ragdoc/`):** Document indexing and vector similarity search.

## 📋 Prerequisites

-   Python 3.10+
-   PostgreSQL with `pgvector` extension
-   Docker & Docker Compose (recommended for easy DB setup)
-   OpenRouter API Key (or compatible OpenAI API)

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd Multi-Source-RAG
```

### 2. Environment Variables
Create a `.env` file in the root directory. You can copy the example:
```bash
cp example_env .env
```

Edit `.env` with your credentials. **New:** You can now configure file paths directly in the `.env` file to avoid hardcoding.

```env
# AI Provider
OPENROUTER_API_KEY=your_api_key_here

# Main Database
DB_NAME=ragsql_db
DB_USER=ragsql_user
DB_PASSWORD=ragsql_pass
DB_HOST=localhost
DB_PORT=5432

# Chat History Database
CHAT_HISTORY_NAME=history_db
CHAT_HISTORY_USER=history_user
CHAT_HISTORY_PASSWORD=history_pass
CHAT_HISTORY_HOST=localhost
CHAT_HISTORY_PORT=5433

# Vector Database
VECTOR_NAME=vector_db
VECTOR_USER=vector_user
VECTOR_PASSWORD=vector_pass
VECTOR_HOST=localhost
VECTOR_PORT=5434

# [OPTIONAL] Paths - Defaults are used if not set
# Path to your local SentenceTransformer model (snapshot folder)
# EMBEDDING_MODEL_PATH=/path/to/local/huggingface/snapshot
# Path to the source document for indexing
# DOC_PATH=./security_incident_guide.md
```

### 3. Install Dependencies
```bash
python -m venv .venv
# Activate venv: .venv\Scripts\activate (Windows) or source .venv/bin/activate (Linux/Mac)
pip install -r requirement.txt
```

### 4. Initialize System
Start the services using Docker Compose and run the initialization script. This script will:
1.  Connect to the running databases.
2.  Initialize the structured SQL database with sample incident data.
3.  Index the documentation (`security_incident_guide.md`) into the vector database.

```bash
docker-compose up -d
python init_system.py
```

*Note: The chat history database is automatically initialized by the container on startup.*

## 🛠️ Usage

### Run the Web UI
The recommended way to interact with Ongkhot.
```bash
streamlit run streamlit_app.py
```

### Run the CLI
For quick testing and debugging.
```bash
python main.py
```

## 📂 Project Structure

```text
Multi-Source-RAG/
├── core/                   # Shared infrastructure (Config, LLM, History)
├── handlers/               # Route handlers (Doc vs SQL)
├── ragdoc/                 # Document RAG logic (Indexing, Retrieval)
├── ragsql/                 # SQL RAG logic (NL2SQL, Execution)
├── utils/                  # Helper functions (Intent, Data Gen)
├── prompt_templates/       # LLM prompts
├── tests/                  # Unit and Integration tests
├── main.py                 # CLI Entry point
├── streamlit_app.py        # Web App Entry point
└── ...
```

## 🧪 Testing
Run unit and integration tests using `pytest`:
```bash
pytest
```

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.