import sqlite3  
# Python's built-in library for working with SQLite databases.

from pathlib import Path  
# Makes working with file paths easier.

# This is where my database file will be stored.
DATABASE_PATH = Path("scheduler.db")

# Create and return a connection to our SQLite database."
def get_connection() -> sqlite3.Connection:
    
    # Open a connection to the database.
    connection = sqlite3.connect(DATABASE_PATH)
    return connection