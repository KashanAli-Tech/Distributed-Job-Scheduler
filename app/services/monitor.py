from threading import Lock


class Monitor:
    
    def __init__(self):
        self.lock = Lock()
        self.total_jobs = 0
        self.success_jobs = 0
        self.failed_jobs = 0

    # called when a job succeeds
    def record_success(self):
        
        with self.lock:
            self.total_jobs += 1
            self.success_jobs += 1

    # called when a job fails permanently
    def record_failure(self):
        
        with self.lock:
            self.total_jobs += 1
            self.failed_jobs += 1

    # return current system stats
    def snapshot(self):
        
        with self.lock:
            return {
                "total_jobs": self.total_jobs,
                "success_jobs": self.success_jobs,
                "failed_jobs": self.failed_jobs
            }