from app.models.job import Job, JobStatus
from app.persistence.job_store import save_job

# Submit a job into the scheduler, update the status, and add it to priority queue
def submit_job(job: Job, system):
  
    # The API has accepted the job, so mark it as queued.
    job.status = JobStatus.QUEUED

    # Save the job in the database before doing anything else.
    save_job(job)

    # Store the job in the shared in-memory registry.
    system.registry[job.id] = job

    # Add the job to the priority queue so a worker can process it.
    system.queue.put(job)

    # Return the updated job object.
    return job