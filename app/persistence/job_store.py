import json 

from app.persistence.database import get_connection, database_lock
from app.models.job import Job, JobPriority, JobStatus

# As the name suggests, this function saves a job to database
def save_job(job: Job):
    
    # using database lock so that only one worker can write to SQLite at a time.
    with database_lock:

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
 
    with database_lock:

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
                result = ?,
                error = ?
            WHERE id = ?
            """,
            (
                (
                job.status.value,
                job.retries,

                # Save the job result as JSON text and If there isn't a result yet, save NULL instead.
                json.dumps(job.result) if job.result is not None else None,

                # Save an error message if one exists. getattr(...) safely returns None if the Job doesn't have an "error" attribute yet.
                getattr(job, "error", None),
                
                job.id,
    )
            ),
        )

        connection.commit()
        connection.close()

# Loads jobs that were not completed before a restart.
def load_unfinished_jobs():

    connection = get_connection()
    cursor = connection.cursor()

    # Find jobs that were not finished.
    cursor.execute(
        """
        SELECT
            id,
            type,
            payload,
            priority,
            status,
            retries,
            max_retries,
            result,
            error
        FROM jobs
        WHERE status IN (?, ?, ?)
        """,
        
            (
            # Only recover jobs that were not finished.
            JobStatus.PENDING.value,
            JobStatus.QUEUED.value,
            JobStatus.RUNNING.value,
        
        ),
    )

    rows = cursor.fetchall()
    connection.close()

    jobs = []

    # Convert database rows back into Job objects.
    for row in rows:

        job = Job(
            id=row["id"],
            type=row["type"],
            payload=json.loads(row["payload"]),
            priority=JobPriority(row["priority"]),
            status=JobStatus(row["status"]),
            retries=row["retries"],
            max_retries=row["max_retries"],

            # Convert result back if it exists.
            result=json.loads(row["result"]) if row["result"] else None,

            error=row["error"],
        )

        jobs.append(job)

    return jobs