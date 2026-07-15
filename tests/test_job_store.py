from app.persistence.job_store import save_job, load_unfinished_jobs
from app.models.job import Job


def test_save_and_load_job():

    job = Job(type="math")
    save_job(job)
    jobs = load_unfinished_jobs()

    assert len(jobs) >= 1
    assert jobs[0].id == job.id