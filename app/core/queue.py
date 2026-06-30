from collections import deque


class JobQueue:
    # simple FIFO queue to hold all incoming jobs
    # using deque because it's fast for append + pop from left

    def __init__(self):
        self.queue = deque()

    def add_job(self, job):
        # adding job to the end of the queue
        self.queue.append(job)

    def get_job(self):
        # taking job from front 
        if self.queue:
            return self.queue.popleft()
        return None

    def size(self):
        # just to check how many jobs are waiting
        return len(self.queue)