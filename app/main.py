from fastapi import FastAPI

from app.api.routes import router
from app.core.system import System
from app.persistence.database import get_connection
from app.persistence.tables import create_tables

# create FastAPI app
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# to allow the React frontend to communicate with the FastAPI backend 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create one system instance with 3 workers for now
system = System(worker_count=3)
app.state.system = system

# register API routes
app.include_router(router)

# starts the distributed worker pool
@app.on_event("startup")
def startup():
    
    create_tables()

    print("Starting Job Scheduler: ")
    system.start()
    
    connection = get_connection()
    connection.close()

