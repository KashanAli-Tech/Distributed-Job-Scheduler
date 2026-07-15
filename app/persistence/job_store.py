import json 

from app.persistence.database import get_connection, database_lock
from app.models.job import Job, JobPriority, JobStatus

# saves a job to database
def save_job(job: Job, database_path=None):
    
    with database_lock:

        connection = get_connection(database_path)
        cursor = connection.cursor()

        # executes the sql query to save a job into database
        cursor.execute(
            """
            INSERT INTO jobs (id,
                type,
                payload,
                priority,
                status,
                retries,
                max_retries,
                result,
                error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
            """,  
            (
                job.id,
                job.type,

                # convert dictionary into JSON text
                json.dumps(job.payload),
                job.priority.value,
                job.status.value,
                job.retries,
                job.max_retries,

                job.result,

                # error starts as None aswell
                None,
            ),
        )

        connection.commit()
        connection.close()

# update an existing job in the database.
def update_job(job: Job, database_path=None):
 
    with database_lock:
        connection = get_connection(database_path)
        cursor = connection.cursor()

        # executes the sql query to update a job from database
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
                
                job.status.value,
                job.retries,
                # save the job result as JSON text and If there isn't a result yet, save as NULL
                json.dumps(job.result) if job.result is not None else None,
                # returns None if the job doesn't have an "error" attribute yet
                getattr(job, "error", None),
                job.id,
            ),
        )

        connection.commit()
        connection.close()

# loads jobs that were not completed before a restart.
def load_unfinished_jobs(database_path=None):

    connection = get_connection(database_path)
    cursor = connection.cursor()

        # executes the sql query to find unfinished jobs
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
            JobStatus.PENDING.value,
            JobStatus.QUEUED.value,
            JobStatus.RUNNING.value,
        
        ),
    )

    rows = cursor.fetchall()
    connection.close()
    jobs = []

    # convert database rows back into Job objects.
    for row in rows:

        job = Job(
            id=row["id"],
            type=row["type"],
            payload=json.loads(row["payload"]),
            priority=JobPriority(row["priority"]),
            status=JobStatus(row["status"]),
            retries=row["retries"],
            max_retries=row["max_retries"],
            result=json.loads(row["result"]) if row["result"] else None,
            error=row["error"],
        )
        jobs.append(job)
    return jobs