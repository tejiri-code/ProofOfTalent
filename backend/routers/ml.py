from fastapi import APIRouter
import subprocess

router = APIRouter(prefix="/ml")

@router.get("/run")
def run_model():
    return {"status": "ML endpoint working"}
