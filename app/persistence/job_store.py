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