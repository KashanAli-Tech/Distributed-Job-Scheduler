from fastapi import FastAPI

from app.api.routes import router
from app.core.system import System
from app.persistence.database import get_connection
from app.persistence.tables import create_tables

# To test that main.py is successfully loaded
print("MAIN.PY LOADED")
# Create FastAPI app
app = FastAPI()

# Create ONE system instance
system = System(worker_count=3)

# Save it inside FastAPI so every route can access it
app.state.system = system

# Register API routes
app.include_router(router)

# Starts the distributed worker pool.
@app.on_event("startup")
def startup():
    
    create_tables()

    print("Starting Job System...")
    system.start()
    
    # connection to the database and closing it straigth away for now
    connection = get_connection()
    connection.close()

