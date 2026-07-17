from fastapi import APIRouter, Request
from app.models.job import Job
from app.services.job_service import submit_job as submit_job_service
from app.monitoring.event_store import get_events
from app.monitoring.retry_store import get_retries
from app.monitoring.failure_store import get_failed_jobs

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
        "payload": job.payload, 
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

@router.get("/jobs")
def get_jobs(request: Request):
    # returns a list of jobs

    system = request.app.state.system

    return [
        {
            "id": job.id,
            "type": job.type,
            "priority": job.priority,
            "status": job.status,
            "retries": job.retries,
            "result": job.result,
        }
        for job in system.registry.values()
    ]

@router.get("/events")
def get_system_events():
    # returns live event logs
    return get_events()

@router.get("/retries")
def get_retry_history():
    # returns retry history
    return get_retries()

@router.get("/failed-jobs")
def failed_jobs():
    # returns failed jobs
    return get_failed_jobs()