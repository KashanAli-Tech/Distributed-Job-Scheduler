from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Optional, Any
from enum import Enum


# using Enum to preventing errors from using invalid values. 
class JobPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# once again, using Enum to preventing errors from using invalid values.
class JobStatus(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"



class Job(BaseModel):
    # unique id generated for every new job and formatted as string
    id: str = Field(default_factory=lambda: str(uuid4()))
    # decides what kind of work this job will do
    type: str
    
    # extra data needed for the job
    # By using Field, it creates a new empty dictionary for every new job
    payload: dict = Field(default_factory=dict)

    # result will be filled later by worker
    result: Optional[Any] = None
    # reason why a job failed
    error: Optional[str] = None
    # priority of the job
    priority: JobPriority = JobPriority.MEDIUM

    # current state of the job
    status: JobStatus = JobStatus.PENDING

    retries: int = 0
    max_retries: int = 3
