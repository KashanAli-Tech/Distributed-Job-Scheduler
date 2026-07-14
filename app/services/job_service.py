from app.models.job import Job, JobStatus
from app.persistence.job_store import save_job, update_job

# submit a job into the schedular, update the status and add it to priority queue
def submit_job(job: Job, system):
  
    job.status = JobStatus.QUEUED
    save_job(job)
    system.registry[job.id] = job
    system.queue.put(job)
    return job

# update the state of job in database
def update_job_state(job: Job):

    update_job(job)
    return job