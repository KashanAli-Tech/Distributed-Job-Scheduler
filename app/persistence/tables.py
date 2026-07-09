from app.persistence.database import get_connection

# Create the database tables if they do not already exist.
def create_tables():
    
    # Open a connection to SQLite.
    connection = get_connection()

    # send SQL commands to the database.
    cursor = connection.cursor()

    # Create our jobs table.
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

    # Save the table creation.
    connection.commit()

    # Close the database connection.
    connection.close()