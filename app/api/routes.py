from fastapi import APIRouter, Request
from app.models.job import Job
from app.services.job_service import submit_job as submit_job_service

router = APIRouter()
# shared queue instance so API + worker use same data


@router.post("/submit-job")
def submit_job(job: Job, request: Request):
    # API endpoint where user sends job data

    # Get the running System instance from FastAPI
    system = request.app.state.system

    # The service handles saving, registry, and queue operations.
    submit_job_service(job, system)


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

@router.get("/metrics")
def get_metrics(request: Request):
    # Returns system-wide monitoring data

    # Get the running System instance from the FastAPI application
    system = request.app.state.system

    
    return {
        # Show how many jobs are waiting in each priority queue
        "queue_sizes": {
            "high": len(system.queue.high),
            "medium": len(system.queue.medium),
            "low": len(system.queue.low),
        },

        # Show how many jobs each worker has processed
        "workers": system.get_worker_stats(),

        # Show overall system metrics (successes, failures, total jobs, etc.)
        "monitor": system.monitor.snapshot()
    }