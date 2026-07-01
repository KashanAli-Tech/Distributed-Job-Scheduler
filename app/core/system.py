from app.core.queue import Queue
from app.core.worker import Worker

# central job storage (single source of truth)
jobs = {}

# shared queue
queue = Queue()

# worker gets everything injected (NO imports back into system inside worker)
worker = Worker(queue, jobs)