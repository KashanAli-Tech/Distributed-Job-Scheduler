from app.persistence.job_store import save_job, load_unfinished_jobs
from app.models.job import Job


def test_save_and_load_job(temp_database):

    job = Job(
        type="math",
        payload={"data": [1, 2, 3]}
    )
    save_job(job, temp_database)
    jobs = load_unfinished_jobs(temp_database)

    assert len(jobs) >= 1
    assert jobs[0].id == job.id

