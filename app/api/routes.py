from core.queue import Queue
from models.job import Job

queue = Queue()  # shared instance

def submit_job(data):
    job = Job()
    queue.add_job(job)

    