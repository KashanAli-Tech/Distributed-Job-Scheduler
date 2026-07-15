import pytest
import threading

from app.models.job import Job, JobPriority
from app.core.queue import PriorityQueue
from app.persistence.database import get_connection
from app.persistence.tables import create_tables

# fake version of actual monitor for testing 
class FakeMonitor:
    def __init__(self):
        self.success_count = 0
        self.failure_count = 0

    def record_success(self):
        self.success_count += 1

    def record_failure(self):
        self.failure_count += 1

# fake version of actual system for testing 
class FakeSystem:
    def __init__(self):
        self.registry = {}
        self.queue = PriorityQueue()
        self.registry_lock = threading.Lock()
        self.monitor = FakeMonitor()


@pytest.fixture
def system():
    return FakeSystem()

# the sample job which i will be using throughout tests
@pytest.fixture
def sample_job():
    return Job(
        type="math",
        payload={"data": [1, 2, 3]},
        priority=JobPriority.HIGH
    )

# the temporary database on which i will be performing tests
@pytest.fixture
def temp_database(tmp_path):

    database_file = tmp_path / "test_scheduler.db"
    create_tables(database_file)    
    return database_file