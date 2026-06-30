from app.core.queue import JobQueue
from app.core.worker import Worker


# One shared queue for the whole application
queue = JobQueue()
# A central variable that stores all the jobs
jobs = {}

# Worker uses that same queue
worker = Worker(queue)