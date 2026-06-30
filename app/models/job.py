from pydantic import BaseModel, Field
from uuid import uuid4


class Job(BaseModel):
    # unique id generated for every new job
    id: str = Field(default_factory=lambda: str(uuid4()))

    # decides what kind of work this job will do
    type: str

    # extra data needed for the job
    payload: dict = Field(default_factory=dict)

    # current state of the job
    status: str = "pending"