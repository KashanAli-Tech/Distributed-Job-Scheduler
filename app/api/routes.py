from fastapi import APIRouter, Request
from app.models.job import Job, JobStatus

router = APIRouter()
# shared queue instance so API + worker use same data


@router.post("/submit-job")
def submit_job(job: Job, request: Request):
    # API endpoint where user sends job data

    # Get the running System instance from FastAPI
    system = request.app.state.system

    # Job has been accepted by the API
    job.status = JobStatus.QUEUED

    # Store job in shared registry
    system.registry[job.id] = job

    # Add job into the shared priority queue
    system.queue.put(job)


    # return a message that job is submitted along with job_id, priority and status
    return {
        "message": "Job submitted successfully",
        "job_id": job.id,
        "priority": job.priority,
        "status": job.status
    }


@router.get("/job/{job_id}")
def get_job(job_id: str, request: Request):
    # Get the latest information about a job.

    # Access the running System
    system = request.app.state.system

    # Look up the job
    job = system.registry.get(job_id)

    # Job doesn't exist
    if job is None:
        return {"error": "Job not found"}

    # Return current job information
    return {
        "id": job.id,
        "type": job.type,
        "priority": job.priority,
        "status": job.status,
        "result": job.result,
        "retries": job.retries
    }