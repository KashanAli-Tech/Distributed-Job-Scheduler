from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Optional, Any
from enum import Enum

class JobPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class JobStatus(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class Job(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: str
    payload: dict = Field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None
    priority: JobPriority = JobPriority.MEDIUM
    status: JobStatus = JobStatus.PENDING
    retries: int = 0
    max_retries: int = 3
