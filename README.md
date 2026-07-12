# Distributed Job Scheduler

A backend project built with Python and FastAPI to explore how applications handle background tasks, queues, workers, and failures. The idea behind this project came from wanting to understand what happens when an application needs to run tasks that should not block the main API. Instead of processing everything immediately, jobs are placed into a queue and handled by background workers. I built this project in stages, gradually adding features such as priority scheduling, multiple workers, retries, and database recovery to understand how more reliable systems are designed.

---

# Features

## Background Job Processing

Jobs are submitted through a FastAPI API and processed separately by worker threads.

```
API Request
     |
Job Queue
     |
Worker Pool
     |
Task Execution
     |
Update Job Status
```

This separates job submission from execution, allowing tasks to run in the background.

---

## Priority Queue

Jobs are assigned different priority levels:

- High
- Medium
- Low

The scheduler uses these priorities to decide which jobs should be processed first.

---

## Multiple Workers

The system uses a worker pool to process multiple jobs concurrently. I am using 3 workers for now but I will add more in future.

Example:

```
Worker-1
Worker-2
Worker-3
```

Each worker is responsible for:

- Taking jobs from the queue
- Running the task
- Updating the job status
- Saving results

Thread locks are used when accessing shared data to reduce conflicts between workers.

---

## Failure Handling

Jobs can fail during execution, allowing the system to test how failures are handled.

If a job fails:

```
RUNNING → FAILED → QUEUED → RUNNING
```

The scheduler retries the job until the maximum retry limit is reached.

If all retries fail, the job is marked as permanently failed.

---

## Database Persistence & Recovery

Earlier versions of the project stored jobs only in memory, meaning all information would be lost after restarting the application.

To solve this, SQLite persistence was introduced.

The database stores:

- Job details
- Current status
- Priority
- Retry attempts
- Results
- Errors

When the application starts, unfinished jobs are recovered and added back into the queue.

---

# System Architecture

```
                 User
                   |
              FastAPI API
                   |
              Job Service
                   |
        -----------------------
        |                     |
 Priority Qeueu        SQLite Database
        |
   Worker Pool
        |
   -------------
   |     |     |
  W1    W2    W3
        |
   Job Execution
```

---

# Development Phases

This project was built incrementally rather than all at once.

## Phase 1: Basic Scheduler

Created the foundation:

- FastAPI API
- Job submission
- Basic task execution
- Job tracking

---

## Phase 2: Queue & Workers

Moved task execution away from the API layer.

Implemented:

- Job queue
- Background workers
- Asynchronous processing

---

## Phase 3: Improving Reliability

Focused on making the scheduler more realistic.

Added:

- Multiple workers
- Priority scheduling
- Retry handling
- Logging
- Monitoring

---

## Phase 4: Persistence & Recovery

Focused on making the system more resilient.

Added:

- SQLite database storage
- Job recovery after restart
- Database locking for concurrent updates

---

# API Endpoints

## Submit Job

```
POST /submit-job
```

Creates a new job and places it into the scheduler.

---

## View Job

```
GET /job/{job_id}
```

Returns information about a job:

- Status
- Result
- Error details
- Retry count

---

## Metrics

```
GET /metrics
```

Displays information about:

- Queue size
- Worker activity
- Job statistics

---

# Tech Stack

- Python
- FastAPI
- SQLite
- Pydentic
- Threading
- UUID
- Logging

---

# Future Improvements

## Phase 5: Dashboard

A React dashboard connected to the FastAPI backend.

Planned features:

- Submit jobs through a user interface
- View running and completed jobs
- Monitor worker activity
- Visualise scheduler metrics

---

## Possible Future Ideas

- Redis/RabbitMQ message queues
- Separate worker processes
- Distributed workers
- More advanced scheduling strategies

---

# What I Learned

Building this project helped me understand:

- How backend services are structured
- Why queues are useful for background processing
- The challenges of running tasks concurrently
- How systems handle failures and recovery
- The importance of designing software in smaller stages

---

# Current Status

**Phase 4 Complete ✅**

Next step:

Building a React dashboard to monitor and interact with the scheduler.
