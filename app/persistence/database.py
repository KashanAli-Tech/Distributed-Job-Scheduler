import sqlite3  
from pathlib import Path  
import threading


# this is where my database file will be stored.
DATABASE_PATH = Path("scheduler.db")
database_lock = threading.Lock()

# create and return a connection to my SQLite database
def get_connection(database_path=None) -> sqlite3.Connection:

    path = database_path or DATABASE_PATH
    connection = sqlite3.connect(path)
    # this allows database rows to be accessed using column names.
    connection.row_factory = sqlite3.Row
    return connection