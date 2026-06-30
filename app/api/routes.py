from fastapi import APIRouter
from app.models.job import Job
from app.core.system import queue

router = APIRouter()
# shared queue instance so API + worker use same data


@router.post("/submit-job")
def submit_job(job: Job):
    # API endpoint where user sends job data

    # job gets created and pushed into queue
    queue.add_job(job)

    return {
        "message": "job submitted",
        "job_id": job.id,
        "type": job.type
    }