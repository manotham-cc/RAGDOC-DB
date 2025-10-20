# GEMINI.md

## Project Overview

This project, `ragsql`, is a Python-based application that leverages Retrieval-Augmented Generation (RAG) to convert natural language questions into SQL queries. It is designed to interact with a PostgreSQL database, execute the generated queries, and provide a user-friendly summary of the results, with a focus on cybersecurity-related data. The application uses the OpenAI API through `openrouter.ai` for its natural language processing capabilities.

**New Feature: Chat History**

To improve user experience and provide conversational context, the application now includes a chat history feature. Previous interactions within a session are stored in a dedicated PostgreSQL database and used to inform subsequent AI responses.

The core technologies used are:
- Python 3.11+
- PostgreSQL (two instances: one for application data, one for chat history)
- Docker
- OpenAI API

## Building and Running

To build and run this project, follow these steps:

1.  **Start the databases:**
    Use Docker Compose to start both the application database and the chat history database services.

    ```bash
    docker-compose up -d
    ```

2.  **Install dependencies:**
    The project's Python dependencies are listed in `pyproject.toml`. You can install them using `uv`.

    ```bash
    uv pip install -r requirements.txt 
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root of the project and add the following environment variables. These are used to connect to the databases and the OpenAI API.

    ```
    OPENROUTER_API_KEY=<your_openrouter_api_key>
    POSTGRES_DB=ragsql_db
    POSTGRES_USER=ragsql_user
    POSTGRES_PASSWORD=ragsql_pass
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    ```
    For the chat history database, the credentials are hardcoded in `ragsql/config.py` for simplicity in this guide, but for production, these should also be managed via environment variables.

4.  **Run the application:**
    Execute the `main.py` script to start the application. It will prompt you to enter a natural language question.

    ```bash
    python main.py
    ```

## Project Structure

-   `main.py`: The main entry point for the application. It handles user input, generates a session ID, orchestrates the process of converting a natural language question to a SQL query, summarizes the result, and saves the chat history.
-   `docker-compose.yml`: Defines both the application's PostgreSQL database service (`db`) and the separate chat history database service (`chat_history_db`).
-   `init-history-db.sql`: SQL script to initialize the `chat_history` table in the `chat_history_db` service.
-   `pyproject.toml`: The project's configuration file, specifying dependencies and other metadata.
-   `prompt_templates/`: This directory contains the text files for the prompts used to interact with the language model.
    -   `nl2sql_prompt.txt`: The prompt for converting natural language to SQL, now including chat history context.
    -   `summary_prompt.txt`: The prompt for generating a user-friendly summary of the query results, now including chat history context.
-   `ragsql/`: The main Python package containing the application's core logic.
    -   `config.py`: Handles the configuration for both the application database and the chat history database connections, as well as the OpenAI API client.
    -   `schema_loader.py`: Connects to the application database to retrieve the schema and sample data, which are used to provide context to the language model.
    -   `nlq_parser.py`: Responsible for converting the natural language question into a SQL query by interacting with the language model, using chat history for context.
    -   `execute_query.py`: Executes the generated SQL query against the application database.
    -   `summary.py`: Takes the query results and generates a user-friendly summary using the language model, also leveraging chat history for context.
    -   `history.py`: New module to handle saving and retrieving chat history from the dedicated `chat_history_db`.
    -   `llm.py`: Reusable module for interacting with the language model.
    -   `utils/`: A sub-package for utility functions.

## Development Conventions

-   **Configuration:** All configuration is managed through environment variables, loaded using `dotenv`. This includes database credentials and API keys. Note that chat history database credentials are hardcoded in `ragsql/config.py` for this guide.
-   **Modularity:** The application is well-structured, with clear separation of concerns. Each module in the `ragsql` package has a specific responsibility.
-   **Prompts:** The use of separate text files for prompts makes it easy to modify the behavior of the language model without changing the Python code.
-   **Extensibility:** To add support for a new type of data or a different database, you would primarily need to update the `schema_loader.py` to handle the new schema and potentially adjust the prompts in the `prompt_templates` directory.