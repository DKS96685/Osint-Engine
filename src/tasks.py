from celery import Celery
import time

# 1. Initialize the Celery Kitchen Manager
# We tell it exactly where to find the Redis Ticket Counter
celery_app = Celery(
    "osint_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# 2. Define the actual task (The Recipe)
# The @celery_app.task decorator turns this normal function into a background job
@celery_app.task
def run_nmap_scan(job_id: str, target: str):
    print(f"👨‍🍳 Chef picked up ticket {job_id}: Scanning {target}...")
    
    # We simulate a heavy 10-second Nmap scan by forcing Python to sleep
    time.sleep(10) 
    
    print(f"✅ Chef finished ticket {job_id}!")
    
    # Return the results so Celery can save them
    return {"job_id": job_id, "status": "completed"}