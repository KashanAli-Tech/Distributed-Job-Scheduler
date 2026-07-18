# Distributed Job Scheduler

A full-stack distributed job scheduling system I built using Python, FastAPI, React, SQLite, threading, and Docker to explore how modern applications handle background processing, concurrency, failures, and persistent data.

The idea behind this project came from wanting to understand how real systems process large volumes of tasks without blocking the main application. I designed a queue-based architecture where jobs submitted through a FastAPI API are managed by a scheduler, prioritised, and executed asynchronously by a multi-worker system.

I developed the project incrementally, evolving it from a simple in-memory job queue into a more reliable system by implementing priority scheduling, concurrent worker execution, thread-safe resource management, automatic retries, structured logging, monitoring, SQLite persistence, and recovery of unfinished jobs after application restarts.

The final system combines a Python backend with a React dashboard and Docker deployment, allowing users to submit, track, and monitor jobs while the scheduler independently manages execution, failures, and recovery. Through this project, I explored key software engineering concepts including API design, concurrency, fault tolerance, data persistence, and scalable system architecture.

---

# Project Overview

## Application Interface

The project includes a React dashboard connected to the FastAPI backend.

The dashboard allows users to:

- Submit jobs through a web interface
- View job status and results
- Search and filter jobs
- Monitor worker activity
- Track retries and failures
- View live scheduler events

Application screenshots can be found here:

```
docs/screenshots/
```

---

# System Design

System design diagrams can be found here:

```
docs/system-diagrams/
```

The diagrams include:

- Complete system architecture
- Queue architecture
- Worker architecture
- Job lifecycle
- Recovery system
- Monitoring architecture

---

# Features

## Background Job Processing

Jobs are submitted through a FastAPI API and processed separately by background workers.

This prevents long-running tasks from blocking the API.

---

## Priority Scheduling

Jobs can be assigned different priority levels:

- HIGH
- MEDIUM
- LOW

A priority queue is used to determine which jobs should be processed first.

Higher priority jobs are selected before lower priority jobs.

---

## Worker Pool & Concurrency

The scheduler uses multiple worker threads to process jobs concurrently.

Workers are responsible for:

- Retrieving jobs from the queue
- Executing tasks
- Updating job status
- Saving results

Thread locks are used when accessing shared resources to reduce conflicts between workers.

---

## Reliability Features

To make the scheduler more realistic, I added several reliability mechanisms:

- Automatic retries for failed jobs
- Failure tracking
- Structured logging
- Job recovery after restart
- Database persistence

---
## Database Persistence

Originally, jobs were stored only in memory, meaning all information would be lost after restarting the application.

To solve this, SQLite persistence was introduced.

The database stores:

- Job information
- Current status
- Priority
- Payload
- Results
- Errors
- Retry attempts

When the application starts, unfinished jobs are recovered and added back into the queue.

---

# Monitoring System

The scheduler includes a monitoring system to observe runtime behaviour.

The monitoring dashboard displays:

- System health
- Worker activity
- Queue sizes
- Success rates
- Live events
- Retry history
- Failed jobs

Monitoring screenshots can be found in:

```
docs/screenshots/
```

---

# Tech Stack

## Backend

- Python
- FastAPI
- SQLite
- Threading
- Pydantic

## Frontend

- React
- Vite
- Axios
- CSS

## Deployment & Tools

- Docker
- Docker Compose
- Git
- GitHub

---

# Running The Project

## Using Docker

Clone the repository and run:

```bash
docker compose up --build
```

The application will start:

Frontend:

```
http://localhost:5173
```

Backend API:

```
http://localhost:8000
```

FastAPI documentation:

```
http://localhost:8000/docs
```

---

# Development Journey

I built this project in stages to understand how software systems become more reliable over time.

## Phase 1: Basic Scheduler

Created the foundation:

- FastAPI API
- Job submission
- Task execution
- Job tracking

---

## Phase 2: Queues & Workers

Introduced background processing:

- Job queue
- Worker threads
- Priority scheduling
- Concurrent execution

---

## Phase 3: Reliability Improvements

Focused on making the scheduler more realistic:

Added:

- Multiple workers
- Retry handling
- Structured logging
- Monitoring metrics

---

## Phase 4: Persistence & Recovery

Improved system reliability:

Added:

- SQLite database storage
- Job persistence
- Recovery after restart
- Safe concurrent database updates

---

## Phase 5: Dashboard & Deployment

Created a user interface and deployment setup:

Added:

- React dashboard
- Job management interface
- Monitoring dashboard
- Docker containerisation

---

# What I Learned

Building this project helped me understand:

- Why background processing is used in real applications
- How queues and workers communicate
- How concurrent systems handle shared resources
- How failures are managed using retries
- Why persistence is important for reliable systems
- How frontend and backend systems communicate

---

# Future Improvements

Possible improvements I would explore:

- Redis or RabbitMQ message queues
- Distributed worker nodes
- Cloud deployment
- Worker autoscaling
- More advanced scheduling algorithms
- Authentication and user management

---

# Current Status: COMPLETED


The project currently includes:

- FastAPI backend
- Priority queue scheduler
- Multi-worker execution
- Retry handling
- SQLite persistence
- Job recovery
- Monitoring dashboard
- React frontend
- Docker deployment
