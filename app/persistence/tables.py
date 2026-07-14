from app.persistence.database import get_connection

# create the database table if it does not already exist.
def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # execute a sql query to create a table.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            payload TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            retries INTEGER DEFAULT 0,
            max_retries INTEGER NOT NULL,
            result TEXT,
            error TEXT
        )
        """)

    connection.commit()
    connection.close()