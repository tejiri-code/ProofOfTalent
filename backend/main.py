from fastapi import FastAPI
from routers import ml

app = FastAPI()

app.include_router(ml.router)

@app.get("/")
def root():
    return {"message": "Backend running!"}
