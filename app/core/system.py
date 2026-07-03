from app.core.queue import JobQueue
from app.core.worker import Worker

# central job storage (single source of truth)
jobs = {}

# shared queue
queue = JobQueue()

# worker gets everything injected (NO imports back into system inside worker)
worker = Worker(queue, jobs)
print("WORKER INSTANCE ID:", id(worker))
