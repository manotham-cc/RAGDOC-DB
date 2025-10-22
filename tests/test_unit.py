"""Unit tests for the RAGSQL application."""

from ragsql.schema_loader import format_schema

def test_format_schema():
    """Tests the format_schema function."""
    schema_dict = {
        "users": {
            "columns": [
                {"column": "id", "type": "integer"},
                {"column": "name", "type": "text"}
            ],
            "samples": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        }
    }
    formatted_schema = format_schema(schema_dict)
    expected_schema = (
        "Table: users\n  Columns: id (integer), name (text)\n\n  Sample rows:\n\n    - id=1, name=Alice\n\n    - id=2, name=Bob"
    )
    assert formatted_schema == expected_schema

from unittest.mock import patch
from ragsql.nlq_parser import question_to_sql
from ragsql.summary import get_summary

@patch('ragsql.nlq_parser.get_database_schema')
@patch('ragsql.nlq_parser.get_llm_response')
def test_question_to_sql(mock_get_llm_response, mock_get_database_schema):
    """Tests the question_to_sql function."""
    mock_get_database_schema.return_value = {
        "users": {
            "columns": [
                {"column": "id", "type": "integer"},
                {"column": "name", "type": "text"}
            ],
            "samples": []
        }
    }
    mock_get_llm_response.return_value = "SELECT * FROM users;"

    sql_query = question_to_sql("list all users")
    assert sql_query == "SELECT * FROM users;"

@patch('ragsql.summary.execute_sql_query')
@patch('ragsql.summary.get_llm_response')
def test_get_summary(mock_get_llm_response, mock_execute_sql_query):
    """Tests the get_summary function."""
    mock_execute_sql_query.return_value = (['foo'], "SELECT * FROM users;")
    mock_get_llm_response.return_value = "This is a summary."

    summary, sql_query = get_summary("list all users")
    assert summary == "This is a summary."
    assert sql_query == "SELECT * FROM users;"
