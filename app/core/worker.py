import time
import threading
import random

from app.core.queue import PriorityQueue
from app.models.job import JobStatus
from app.persistence.job_store import update_job
from app.monitoring.event_store import add_event
from app.monitoring.retry_store import add_retry
from app.monitoring.failure_store import add_failed_job


class Worker:
    
    def __init__(self, worker_id: int, queue: PriorityQueue, registry: dict, registry_lock: threading.Lock, system):
        self.worker_id = worker_id
        self.queue = queue
        self.system = system
        self.registry = registry
        self.registry_lock = registry_lock
        self.running = True
        self.processed_count = 0


    # debug output for tracing worker behaviour
    def log(self, message: str):
        print(f"[Worker {self.worker_id}] {message}")


    # continuously fetches jobs and processes them.       
    def start(self):
        
        self.log("Started")

        while self.running:
            job = self.queue.get()
            # if no job available, sleep for 0.5 sec
            if not job:
                time.sleep(0.5)
                continue

            self.process_job(job)


    def process_job(self, job):
        
        add_event(f"Worker {self.worker_id} picked job {job.id}", "RUNNING")

        with self.registry_lock:
            job.status = JobStatus.RUNNING
            update_job(job, self.system.database_path)
            self.registry[job.id] = job

        # simulate processing time 
        time.sleep(random.uniform(0.5, 2.0))

  
        # simulate random FAILURE
        failure_chance = 0.3  # 25% failure rate for now
        if random.random() < failure_chance:
            self.handle_failure(job)
            return
        

        result = self.execute_job(job)

        with self.registry_lock:
            job.result = result
            job.status = JobStatus.SUCCESS
            update_job(job, self.system.database_path)
            self.registry[job.id] = job
            self.system.monitor.record_success()

        self.processed_count += 1
        add_event(f"Worker {self.worker_id} completed job {job.id}", "SUCCESS")

    
    # handles retry logic and failure states.
    def handle_failure(self, job):

        with self.registry_lock:
            job.retries += 1
            add_retry(job, "Job execution failed")
            add_event(f"Worker {self.worker_id} failed job {job.id}", "FAILED")

            if job.retries <= job.max_retries:
                job.status = JobStatus.QUEUED
                update_job(job, self.system.database_path)

                # resubmit job for another attempt.
                self.queue.put(job)
                self.log(f"Requeued job {job.id} for retry")

            else:
                job.status = JobStatus.FAILED
                add_failed_job(job, job.error)
                job.error = "Maximum retries exceeded"
                update_job(job, self.system.database_path)
                self.registry[job.id] = job
                self.system.monitor.record_failure()
                self.log(f"Job {job.id} permanently FAILED")
    
    # gives job to correct handler based on type.
    def execute_job(self, job):
        
        if job.type == "sleep":
            return self.handle_sleep(job)

        elif job.type == "math":
            return self.handle_math(job)

        elif job.type == "text":
            return self.handle_text(job)

        return {"error": "unknown job type"}

    # Note: I will add more job handlers as the project expand

    def handle_sleep(self, job):
        time.sleep(job.payload.get("duration", 1))
        return {"status": "slept"}

    def handle_math(self, job):
        data = job.payload.get("data", [])
        return {"result": sum(data)}

    def handle_text(self, job):
        text = job.payload.get("text", "")
        return {"word_count": len(text.split())}
    
    
  
