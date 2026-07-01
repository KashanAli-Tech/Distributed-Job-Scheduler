import time


class Worker:
    def __init__(self, queue, jobs):
        # worker is basically the engine that keeps checking queue forever
        self.queue = queue
        self.jobs = jobs
        self.running = True

    def start(self):
        # infinite loop so worker never stops running
        # constantly checks if there are jobs to process
        while self.running:

            job = self.queue.get_job()

            if job:
                # mark job as running before processing
                job.status = "running"
                self.jobs[job.id] = job

                self.log(job, "running")

                # process job and get result
                result = self.process_job(job)

                # store result
                job.result = result

                # mark as completed after processing
                job.status = "completed"
                self.jobs[job.id] = job

                self.log(job, "completed")

            else:
                # small sleep so CPU doesn't go crazy when queue is empty
                time.sleep(0.5)

    def process_job(self, job):
        # this decides what function to call based on job type
        # kind of like routing inside the worker

        if job.type == "sleep":
            return self.handle_sleep(job)

        elif job.type == "math":
            return self.handle_math(job)

        elif job.type == "text":
            return self.handle_text(job)

        return None

    def handle_sleep(self, job):
        # simulates a task that takes time (like real background work)
        time.sleep(job.payload.get("duration", 1))
        return "slept"

    def handle_math(self, job):
        # simple CPU-style task just to simulate computation
        data = job.payload.get("data", [])
        return sum(data)

    def handle_text(self, job):
        # basic text processing simulation
        text = job.payload.get("text", "")
        return len(text.split())

    def log(self, job, status):
        # just printing state for now, helps debugging
        print(f"[{status}] Job {job.id}")