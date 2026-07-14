from app.models.job import Job, JobPriority


def test_queue_adds_high_priority_job_first(system):
    high_job = Job(
        type="math",
        priority=JobPriority.HIGH
    )

    system.queue.put(high_job)
    result = system.queue.get()

    assert result == high_job

def test_priority_order(system):

    low = Job(type="math", priority=JobPriority.LOW)
    medium = Job(type="math", priority=JobPriority.MEDIUM)
    high = Job(type="math", priority=JobPriority.HIGH)

    system.queue.put(low)
    system.queue.put(medium)
    system.queue.put(high)

    assert system.queue.get() == high
    assert system.queue.get() == medium
    assert system.queue.get() == low

def test_empty_queue_returns_true(system):
    assert system.queue.empty() is True

def test_queue_not_empty_after_add(system, sample_job):
    system.queue.put(sample_job)
    assert system.queue.empty() is False

def test_get_empty_queue_returns_none(system):
    result = system.queue.get()
    assert result is None