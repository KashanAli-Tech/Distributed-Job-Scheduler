from unittest.mock import patch

from app.services.job_service import submit_job
from app.models.job import Job, JobStatus


def test_submit_job_adds_to_queue(system):
    job = Job(type="math")

    with patch(
        "app.services.job_service.save_job"
    ):

        result = submit_job(job, system)


    assert result.status == JobStatus.QUEUED
    assert job.id in system.registry
    assert system.queue.empty() is False


def test_submit_job_saves_job(system):
    job = Job(type="math")

    with patch(
        "app.services.job_service.save_job"
    ) as mock_save:

        submit_job(job, system)
        mock_save.assert_called_once_with(job)