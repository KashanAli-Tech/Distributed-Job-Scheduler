import sqlite3  
from pathlib import Path  


# This is where my database file will be stored.
DATABASE_PATH = Path("scheduler.db")

# Create and return a connection to my SQLite database."
def get_connection() -> sqlite3.Connection:
    
    # Open a connection to the database.
    connection = sqlite3.connect(DATABASE_PATH)

    # Allows database rows to be accessed using column names.
    connection.row_factory = sqlite3.Row
    
    return connection