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

            -- Unique ID for each job
            id TEXT PRIMARY KEY,

            -- The actual task the worker needs to run
            task TEXT NOT NULL,

            -- Job priority 
            priority TEXT NOT NULL,

            -- Current state of the job
            status TEXT NOT NULL,

            -- Number of times this job has been retried
            retries INTEGER DEFAULT 0,

            -- Output returned after successful completion
            result TEXT,

            -- Error message if the job fails
            error TEXT
        )
        """
    )

    # Save the table creation.
    connection.commit()

    # Close the database connection.
    connection.close()