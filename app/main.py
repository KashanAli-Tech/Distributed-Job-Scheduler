from fastapi import FastAPI

from app.api.routes import router

# create FastAPI app instance (this is the main entry point of the API)
app = FastAPI()
# connect API routes (endpoints) to the FastAPI app
app.include_router(router)