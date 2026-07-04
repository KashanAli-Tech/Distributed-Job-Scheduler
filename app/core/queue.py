from collections import deque
from threading import Lock
# using Lock so only worker can access queue at once.

from app.models.job import Job, JobPriority


# A thread-safe priority queue system.
# Workers always check HIGH first → then MEDIUM → then LOW 
class PriorityQueue:

    def __init__(self):
        # Separate queues for each priority level
        self.high = deque()
        self.medium = deque()
        self.low = deque()

        # Lock ensures only ONE worker modifies queue at a time
        self.lock = Lock()


    # Add a job into the correct priority queue.
    def put(self, job: Job):
        
        with self.lock:
            # Mark job as queued when it enters system
            job.status = "QUEUED"

            # Place job into correct queue based on priority

            if job.priority == JobPriority.HIGH:
                self.high.append(job)

            elif job.priority == JobPriority.MEDIUM:
                self.medium.append(job)

            else:
                self.low.append(job)

    # Remove and return the next job to process.
    def get(self):

        with self.lock:
            # Always check HIGH priority first
            if self.high:
                return self.high.popleft()

            # Then MEDIUM priority
            if self.medium:
                return self.medium.popleft()

            # Then LOW priority
            if self.low:
                return self.low.popleft()

            # If no jobs exist
            return None

    def empty(self):
        
        # Check if all queues are empty.
        with self.lock:
            return not (self.high or self.medium or self.low)