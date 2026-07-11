import threading

from app.core.queue import PriorityQueue
from app.core.worker import Worker
from app.services.monitor import Monitor
from app.services.logger import setup_logger
from app.persistence.job_store import load_unfinished_jobs


""" System = orchestrator of the whole job engine. Responsibilities of system:
    create shared queue
    create shared job registry
    start multiple workers
    manage threads """

class System:

    def __init__(self, worker_count: int = 3):
        # shared priority queue for all workers
        self.queue = PriorityQueue()

        # shared job registry (source of truth)
        self.registry = {}

        # lock to protect registry updates
        self.registry_lock = threading.Lock()

        # number of workers in the system
        self.worker_count = worker_count

        # store worker threads
        self.threads = []

        # store worker objects
        self.workers = []

        # Monitoring system
        self.monitor = Monitor()

        # used for logging
        self.logger = setup_logger()


    # Boot the system and launch all workers.
    def start(self):

        self.logger.info("Starting Distributed Job System...")

        recovered_jobs = load_unfinished_jobs()
        for job in recovered_jobs:

            # Restore job in memory registry.
            self.registry[job.id] = job

            # and Put it back into worker queue.
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


    # Expose queue to API layer so jobs can be submitted.
    def get_queue(self):
        return self.queue


    # Expose registry so API can check job status.
    def get_registry(self):
        return self.registry

    # Simple monitoring info 
    def get_worker_stats(self):
        return {
            f"worker-{w.worker_id}": w.processed_count
            for w in self.workers
        }
