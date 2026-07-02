from fastapi import APIRouter
from app.models.job import Job
from app.core.system import queue
from app.core.system import jobs

router = APIRouter()
# shared queue instance so API + worker use same data


@router.post("/submit-job")
def submit_job(job: Job):
    # API endpoint where user sends job data

    # job gets created and pushed into queue
    queue.add_job(job)

    jobs[job.id] = job

    return {
        "message": "job submitted",
        "job_id": job.id,
        "type": job.type
    }

@router.get("/job/{job_id}")
def get_job(job_id: str):
    job = jobs.get(job_id)

    print("DEBUG job:", job)
    print("DEBUG type:", type(job))

    if not job:
        return {"error": "Job not found"}
    
    return {
        "id": job.id,
        "type": job.type,
        "status": job.status ,
        "result": job.result,
        "payload": job.payload
    }