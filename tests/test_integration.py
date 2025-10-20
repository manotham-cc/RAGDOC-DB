"""Integration tests for the RAGSQL application."""

import pytest
from ragsql.config import get_db_connection
from ragsql.llm import get_llm_response

# Note: These tests require a running PostgreSQL database and a valid OPENROUTER_API_KEY.

def test_db_connection():
    """Tests the database connection."""
    conn = get_db_connection()
    assert conn is not None
    conn.close()

@pytest.mark.skip(reason="This test requires a valid OPENROUTER_API_KEY.")
def test_llm_response():
    """Tests the LLM API call."""
    response = get_llm_response("say hello", "hello")
    assert isinstance(response, str)
    assert len(response) > 0
