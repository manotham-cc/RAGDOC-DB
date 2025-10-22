"""This module loads the database schema and formats it for the LLM."""

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
from ragsql.config import get_db_connection

def get_database_schema(conn=None):
    """
    Retrieves the database schema.

    Args:
        conn: An optional database connection object.

    Returns:
        A dictionary representing the database schema.
    """
    conn = get_db_connection()
    if conn is None:
        print("Database connection failed.")
        return {}

    schema = {}
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE';
            """)
            tables = [row[0] for row in cur.fetchall()]

            for table in tables:
                cur.execute("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = %s;
                """, (table,))
                columns = [{"column": c, "type": t} for c, t in cur.fetchall()]

                # fetch up to 3 sample rows for the table
                samples = []
                try:
                    with conn.cursor(cursor_factory=RealDictCursor) as sample_cur:
                        sample_query = sql.SQL("SELECT * FROM {} LIMIT 3").format(sql.Identifier(table))
                        sample_cur.execute(sample_query)
                        for row in sample_cur.fetchall():
                            samples.append(dict(row))
                except Exception:
                    samples = []

                schema[table] = {"columns": columns, "samples": samples}
        print("Schema loaded successfully.")
        return schema
    except psycopg2.Error as e:
        print("Error loading schema:", e)
        return {}
    finally:
        conn.close()

def format_schema(schema_dict):
    """
    Formats the schema dictionary into a string for the LLM context.

    Args:
        schema_dict: A dictionary representing the database schema.

    Returns:
        A formatted string representing the database schema.
    """
    formatted = []
    for table, cols in schema_dict.items():
        column_list = cols.get('columns') if isinstance(cols, dict) else cols
        col_desc = ", ".join([f"{c['column']} ({c['type']})" for c in column_list])
        formatted.append(f"Table: {table}\n  Columns: {col_desc}")

        # include sample rows if present
        samples = cols.get('samples') if isinstance(cols, dict) else None
        if samples:
            formatted.append("  Sample rows:")
            for s in samples:
                # compact representation
                kv = ", ".join([f"{k}={v}" for k, v in s.items()])
                formatted.append(f"    - {kv}")
    return "\n\n".join(formatted)


if __name__ == "__main__":
    schema = get_database_schema()
    if schema:
        formatted = format_schema(schema)
        print(formatted)


