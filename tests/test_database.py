from app.persistence.database import get_connection
import sqlite3


def test_database_connection():

    connection = get_connection()
    assert connection is not None
    connection.close()


def test_database_returns_row_objects():

    connection = get_connection()
    assert connection.row_factory == sqlite3.Row
    connection.close()

def test_database_can_use_custom_path(tmp_path):

    database_file = tmp_path / "test_database.db"
    connection = get_connection(database_file)
    assert connection is not None
    connection.close()
    assert database_file.exists()