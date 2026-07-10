import json 

from app.persistence.database import get_connection
from app.models.job import Job

# As the name suggests, this function saves a job to database
def save_job(job: Job):
    
    connection = get_connection()
    cursor = connection.cursor()

    # Insert the job data into the jobs table.
    cursor.execute(
        """
        INSERT INTO jobs (
            id,
            type,
            payload,
            priority,
            status,
            retries,
            max_retries,
            result,
            error
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
        """,  # parameterised query = SQL structure first, then give values separately
        (
            job.id,
            job.type,

            # Convert dictionary into JSON text
            json.dumps(job.payload),

            # Convert Enum into string
            job.priority.value,

            # Convert Enum into string
            job.status.value,

            job.retries,
            job.max_retries,

            # Result starts as None
            job.result,

            # Error starts as None aswell
            None,
        ),
    )

    connection.commit()
    connection.close()

# Update an existing job in the database.
def update_job(job: Job):
 
    # Open a connection to SQLite.
    connection = get_connection()

    # Cursor allows us to execute SQL commands.
    cursor = connection.cursor()

    # Update the existing job row.
    cursor.execute(
        """
        UPDATE jobs
        SET
            status = ?,
            retries = ?,
            result = ?
        WHERE id = ?
        """,
        (
            # Current job status
            job.status.value,

            # Current retry count
            job.retries,

            # Result after completing the job
            json.dumps(job.result),

            # Find the correct job using its ID
            job.id,
        ),
    )

    connection.commit()
    connection.close()