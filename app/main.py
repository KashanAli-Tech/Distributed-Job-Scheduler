from fastapi import FastAPI
import threading

from app.api.routes import router
from app.core.system import worker
# To test that main.py is successfully loaded
print("MAIN.PY LOADED")

app = FastAPI()
app.include_router(router)


# this runs when FastAPI starts
@app.on_event("startup")
def startup():
    print("Startup Triggered")
    # run worker in background so FastAPI doesn't freeze
    thread = threading.Thread(target=worker.start, daemon=True)
    thread.start()

