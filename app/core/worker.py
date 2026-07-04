import time
import threading
import random

from app.core.queue import PriorityQueue
from app.models.job import JobStatus

""" Worker = simulated "node" in a distributed system. It:
     pulls jobs from shared queue
     processes them
     may fail randomly
     retries failed jobs
     updates shared registry safely """
class Worker:
    

    def __init__(self, worker_id: int, queue: PriorityQueue, registry: dict, registry_lock: threading.Lock):
        self.worker_id = worker_id
        self.queue = queue

        # shared job storage
        self.registry = registry

        # protects shared dict updates
        self.registry_lock = registry_lock

        # worker state
        self.running = True
        self.processed_count = 0

    # Standard debug output for tracing worker behaviour
    def log(self, message: str):
        print(f"[Worker-{self.worker_id}] {message}")


    # Main worker loop.
    # Continuously fetches jobs and processes them.       
    def start(self):
        
        self.log("Started")

        while self.running:

            # get next available job (priority aware)
            job = self.queue.get()

            # if no job available, sleep
            if not job:
                time.sleep(0.5)
                continue

            self.process_job(job)


    # Full lifecycle handler:
    # RUNNING then SUCCESS or FAILED (with retry logic)
    def process_job(self, job):
        

        self.log(f"Picked job {job.id}")

        # mark job as RUNNING (safe update)
        with self.registry_lock:
            job.status = JobStatus.RUNNING
            self.registry[job.id] = job

        # simulate processing time 
        time.sleep(random.uniform(0.5, 2.0))

  
        # simulate random FAILURE
        failure_chance = 0.25  # 25% failure rate

        # Generate a random number between 0 and 1 and
        # If it's less than 0.25, we simulate a job failure
        if random.random() < failure_chance:
            self.handle_failure(job)

            # Stop processing this job immediately
            # (we don't continue to success path)
            return

        # If the the job didn't fail, then SUCCESS PATH
        result = self.execute_job(job)

        with self.registry_lock:
            job.result = result
            job.status = JobStatus.SUCCESS
            self.registry[job.id] = job

        self.processed_count += 1
        self.log(f"Completed job {job.id}")

    
    # Handles retry logic and failure states.
    def handle_failure(self, job):

        with self.registry_lock:
            job.retries += 1

            self.log(f"Job {job.id} FAILED (retry {job.retries})")

            # RETRY LOGIC
            if job.retries <= job.max_retries:
                job.status = JobStatus.QUEUED

                # push job back into queue for retry
                self.queue.put(job)
                self.log(f"Re-queued job {job.id} for retry")

            else:
                # FINAL FAILURE - Declare the job as FAILED
                job.status = JobStatus.FAILED
                self.registry[job.id] = job

                self.log(f"Job {job.id} permanently FAILED")

    
    # Routes job to correct handler based on type.
    def execute_job(self, job):
        
        if job.type == "sleep":
            return self.handle_sleep(job)

        elif job.type == "math":
            return self.handle_math(job)

        elif job.type == "text":
            return self.handle_text(job)

        return {"error": "unknown job type"}

    # JOB HANDLERS - Need to add more as the project expand

    def handle_sleep(self, job):
        time.sleep(job.data.get("duration", 1))
        return {"status": "slept"}

    def handle_math(self, job):
        data = job.data.get("data", [])
        return {"result": sum(data)}

    def handle_text(self, job):
        text = job.data.get("text", "")
        return {"word_count": len(text.split())}