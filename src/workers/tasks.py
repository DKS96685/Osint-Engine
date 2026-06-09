# src/workers/tasks.py — The Chefs (Celery Workers)
import os
import time
from celery import Celery

from src.database import SessionLocal
from src.model import ScanJob

# Read broker/backend URLs from environment, falling back to localhost for local dev
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Initialize the Celery "kitchen manager"
celery_app = Celery(
    "osint_tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

# Optional: Celery configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)


@celery_app.task(bind=True, name="src.workers.process_osint_scan")
def process_osint_scan(self, job_id: str, target: str):
    """
    The 'Recipe' — performs the actual OSINT scan.
    This runs in the background so the API (the Waiter) stays responsive.
    """
    print(f"👨‍🍳 Chef picked up ticket {job_id}: Scanning {target}...")

    # Update DB status to 'processing'
    try:
        db = SessionLocal()
        job = db.query(ScanJob).filter(ScanJob.id == job_id).first()
        if job:
            job.status = "processing"
            db.commit()
        db.close()
    except Exception as e:
        print(f"DB update error: {e}")

    # TODO: Replace this simulation with real scanning logic (nmap, dns, etc.)
    time.sleep(10)

    # Update DB status to 'completed'
    try:
        db = SessionLocal()
        job = db.query(ScanJob).filter(ScanJob.id == job_id).first()
        if job:
            job.status = "completed"
            db.commit()
        db.close()
    except Exception as e:
        print(f"DB update error: {e}")

    print(f"✅ Chef finished ticket {job_id}!")
    return {"job_id": job_id, "target": target, "status": "completed"}
