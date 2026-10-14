from fastapi import FastAPI
from app.database import init_db

app = FastAPI()
init_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}