from collections import deque
from threading import Lock

from app.models.job import Job, JobPriority


class PriorityQueue:

    def __init__(self):
        self.high = deque()
        self.medium = deque()
        self.low = deque()
        self.lock = Lock()


    # add a job into the correct priority queue.
    def put(self, job: Job):
        
        with self.lock:
            job.status = "QUEUED"

            if job.priority == JobPriority.HIGH:
                self.high.append(job)

            elif job.priority == JobPriority.MEDIUM:
                self.medium.append(job)

            else:
                self.low.append(job)

    # remove and return the next job to process.
    def get(self):

        with self.lock:
            if self.high:
                return self.high.popleft()

            if self.medium:
                return self.medium.popleft()

            if self.low:
                return self.low.popleft()

            return None

    # check if all queues are empty.
    def empty(self):
        with self.lock:
            return not (self.high or self.medium or self.low)