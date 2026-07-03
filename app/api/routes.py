from fastapi import APIRouter
from app.models.job import Job
from app.core.system import queue, jobs

router = APIRouter()
# shared queue instance so API + worker use same data


@router.post("/submit-job")
def submit_job(job: Job):
    # API endpoint where user sends job data

    # job gets created and pushed into queue
    queue.add_job(job)

    # so now job means the specific job being handled at the time
    jobs[job.id] = job

    # return a message that job is submitted along with id and type.
    return {
        "message": "job submitted",
        "job_id": job.id,
        "type": job.type
    }


@router.get("/job/{job_id}")
def get_job(job_id: str):
    # get job from memory using id
    job = jobs.get(job_id)

    print("DEBUG job:", job)
    print("DEBUG type:", type(job))

    # if job doesn't exist, return error
    if not job:
        return {"error": "Job not found"}
    
    # return job details
    return {
        "id": job.id,
        "type": job.type,
        "status": job.status,
        "result": job.result,
        "payload": job.payload
    }