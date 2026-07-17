failed_jobs = []


def add_failed_job(job, error):

    failed_jobs.append(
        {
            "job_id": job.id,
            "type": job.type,
            "error": error or "Unknown execution failure",
            "retries": job.retries
        }
    )


def get_failed_jobs():

    return failed_jobs[-50:]