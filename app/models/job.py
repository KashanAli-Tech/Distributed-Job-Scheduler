from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Optional, Any


class Job(BaseModel):
    # unique id generated for every new job and formatted as string
    id: str = Field(default_factory=lambda: str(uuid4()))
    # decides what kind of work this job will do
    type: str
    # extra data needed for the job
    # By using Field, it creates a new empty dictionary for every new job
    payload: dict = Field(default_factory=dict)
    # current state of the job
    status: str = "pending"
    # result will be filled later by worker
    result: Optional[Any] = None
