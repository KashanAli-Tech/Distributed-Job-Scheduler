# Distributed Job Scheduler 

## Overview

This project is a Python-based distributed job scheduling system built using FastAPI. The goal is to understand how real-world backend systems handle background processing, concurrency, and fault tolerance.

It is inspired by systems like Celery, AWS SQS, and general worker-based architectures used in production systems.

The project is being developed in phases, with each phase gradually adding more realistic distributed systems behaviour.

---

## Current Status

**Phase 3 Complete**

At this stage, the system simulates a multi-worker job processing engine with basic fault tolerance and observability features.

It is not production-ready, but it demonstrates the core ideas behind distributed job processing systems.

---

## Key Features (Phase 3)

### Multi-Worker Processing

- Multiple worker threads process jobs concurrently
- Workers share a common job queue
- Ensures no duplicate processing of jobs

---

### Priority-Based Scheduling

Jobs are processed based on priority:

- HIGH
- MEDIUM
- LOW

Higher priority jobs are handled before lower priority ones.

---

### Job Lifecycle

Each job moves through a defined lifecycle:

```
PENDING → QUEUED → RUNNING → SUCCESS
```

If failures occur:

```
RUNNING → FAILED → (retry if available)
```

---

### Fault Tolerance (Simulated)

To mimic real-world system behaviour:

- Jobs can fail randomly during execution
- Failed jobs are retried up to a fixed limit
- Jobs exceeding retry limits are marked as failed permanently

---

### Observability

The system includes basic monitoring features:

- Total jobs processed
- Successful vs failed jobs
- Worker-level job counts
- Queue size breakdown by priority

---

### Logging

Structured logging has been added to help track system behaviour, including:

- Worker startup events
- Job execution flow
- Failures and retries
- Completion states

---

### REST API

Built using FastAPI:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/submit-job` | Submit a new job |
| GET | `/job/{job_id}` | Get job status |
| GET | `/metrics` | View system metrics |

---

## Architecture (High Level)

```
FastAPI API Layer
        ↓
System Orchestrator
        ↓
Priority Queue
        ↓
Worker Pool (Threads)
        ↓
Shared Job Registry
```

---

## Technologies Used

- Python
- FastAPI
- Pydantic
- Threading
- Logging
- UUID
- Collections (deque)

---

## Software Development Approach

This project follows an **iterative development approach (similar to incremental SDLC)**.

Instead of building everything at once, the system is developed step-by-step in phases. Each phase introduces new features while improving the architecture.

This makes it easier to:

- Understand system design progressively
- Test individual components in isolation
- Refactor safely as complexity increases

---

## Limitations (Current Phase)

This system is still a learning implementation and has some limitations:

- In-memory only (no persistence)
- Workers run as threads, not separate processes
- No distributed messaging system (e.g. Redis, Kafka)
- No persistence across restarts

These are intentionally left for future phases.

---

## Planned Future Improvements

### Phase 4 (Planned)

- Introduce Redis-based queueing
- Persistent job storage (SQLite or Redis)
- Job recovery after restart

---

### Phase 5 (Planned)

- Real-time monitoring dashboard
- WebSocket-based updates
- Live job tracking interface

---

### Phase 6 (Long-term ideas)

- Distributed worker processes (multi-machine simulation)
- Advanced scheduling policies
- Dead-letter queues
- Rate limiting and backpressure handling

---

## Learning Outcomes

This project helped me understand:

- How job queues work internally
- How concurrency is managed with threads
- Basic distributed systems design concepts
- Fault tolerance through retries
- System observability and monitoring

The focus is on understanding **how these systems work under the hood**, rather than building a production-grade replacement.

---

## Final Note

This is an educational project and is still evolving. The goal is to gradually move from a simple API-based system to a more realistic distributed job processing architecture over time.
