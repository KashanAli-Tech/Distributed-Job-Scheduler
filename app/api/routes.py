from fastapi import APIRouter, Request
from app.models.job import Job
from app.services.job_service import submit_job as submit_job_service

# shared queue instance so API + worker use same data
router = APIRouter()

@router.post("/submit-job")
def submit_job(job: Job, request: Request):
    # API endpoint where user sends job data

    system = request.app.state.system
    submit_job_service(job, system)

    return {
        "message": "Job submitted successfully",
        "job_id": job.id,
        "priority": job.priority,
        "status": job.status
    }


@router.get("/job/{job_id}")
def get_job(job_id: str, request: Request):
    # get the latest information about a job.

    system = request.app.state.system

    # look up the job from the registry
    job = system.registry.get(job_id)

    # if the job doesn't exist then raiuse an error
    if job is None:
        return {"error": "Job not found"}

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
    # returns system wide monitoring data

    system = request.app.state.system
    
    return {
        "queue_sizes": {
            "high": len(system.queue.high),
            "medium": len(system.queue.medium),
            "low": len(system.queue.low),
        },
        "workers": system.get_worker_stats(),
        "monitor": system.monitor.snapshot()
    }