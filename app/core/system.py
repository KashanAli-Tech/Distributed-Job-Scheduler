import threading

from app.core.queue import PriorityQueue
from app.core.worker import Worker
from app.services.monitor import Monitor
from app.services.logger import setup_logger
from app.persistence.job_store import load_unfinished_jobs
from app.persistence.database import DATABASE_PATH



class System:

    def __init__(self, worker_count: int = 3):
        
        self.database_path = DATABASE_PATH  # database path support
        self.queue = PriorityQueue() # shared priority queue for all workers
        self.registry = {} # shared job registry
        self.registry_lock = threading.Lock() # lock to protect registry updates
        self.worker_count = worker_count # number of workers in the system
        self.threads = [] # store worker threads
        self.workers = [] # store worker objects
        self.monitor = Monitor() # monitoring system
        self.logger = setup_logger() # used for logging
        


    # boot the system and launch all workers.
    def start(self):

        self.logger.info("Starting Distributed Job System...")

        recovered_jobs = load_unfinished_jobs()
        for job in recovered_jobs:
            self.registry[job.id] = job
            self.queue.put(job)

        self.logger.info(
            f"Recovered {len(recovered_jobs)} unfinished jobs"
        )

        # create workers
        for i in range(self.worker_count):

            worker = Worker(
                worker_id=i + 1,
                queue=self.queue,
                registry=self.registry,
                registry_lock=self.registry_lock,
                system=self)

            self.workers.append(worker)

            # each worker runs in its own thread
            thread = threading.Thread(target=worker.start)

            thread.daemon = True  # allows program to exit cleanly
            self.threads.append(thread)
            thread.start()

            self.logger.info(f"Worker-{i + 1} started")

        self.logger.info("System fully running with worker pool")


    # expose queue to API layer so jobs can be submitted.
    def get_queue(self):
        return self.queue


    # expose registry so API can check job status.
    def get_registry(self):
        return self.registry

    # simple monitoring info 
    def get_worker_stats(self):
        return {
            f"worker-{w.worker_id}": w.processed_count
            for w in self.workers
        }
