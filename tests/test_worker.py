from app.core.worker import Worker
from app.models.job import Job, JobStatus


def create_worker(system):
    return Worker(worker_id=1,
        queue=system.queue,
        registry=system.registry,
        registry_lock=system.registry_lock,
        system=system)


def test_math_job_execution(system):
    worker = create_worker(system)

    job = Job(
        type="math",
        payload={"data": [1,2,3]}
    )
    result = worker.execute_job(job)
    assert result == {"result": 6}


def test_text_job_execution(system):
    worker = create_worker(system)

    job = Job(
        type="text",
        payload={"text": "hello world"}
    )
    result = worker.execute_job(job)
    assert result == {"word_count": 2}


def test_sleep_job_execution(system):
    worker = create_worker(system)

    job = Job(
        type="sleep",
        payload={"duration": 0}
    )
    result = worker.execute_job(job)
    assert result == {"status": "slept"}


def test_unknown_job_execution(system):
    worker = create_worker(system)
    job = Job(type="unknown")
    result = worker.execute_job(job)
    assert result == {"error": "unknown job type"}


def test_failure_requeues_job(system):
    worker = create_worker(system)

    job = Job(
        type="math",
        max_retries=3
    )

    worker.handle_failure(job)
    assert job.status == JobStatus.QUEUED
    assert job.retries == 1


def test_failure_marks_failed_after_max_retries(system):
    worker = create_worker(system)

    job = Job(
        type="math",
        retries=3,
        max_retries=3
    )

    worker.handle_failure(job)
    assert job.status == JobStatus.FAILED
    assert job.error == "Maximum retries exceeded"