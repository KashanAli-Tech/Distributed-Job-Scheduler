from fastapi import FastAPI

from app.api.routes import router
from app.core.system import System

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
    print("Starting Job System...")
    system.start()

