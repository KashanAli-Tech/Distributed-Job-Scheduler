retry_history = []


def add_retry(job, reason):

    retry_history.append(
        {
            "job_id": job.id,
            "attempt": min(job.retries, job.max_retries),
            "max_retries": job.max_retries,
            "reason": reason
        }
    )


def get_retries():

    return retry_history[-50:]