# src/api/main.py — The Waiter (FastAPI)
import uuid
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import engine, get_db, Base
from src.model import ScanJob
from src.schemas import ScanRequest, ScanResponse
from src.workers.tasks import process_osint_scan

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OSINT Engine API",
    description="A high-performance OSINT reconnaissance engine",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict:
    """Quick health check — the Waiter is alive."""
    return {"status": "ok"}


@app.post("/scans/", response_model=ScanResponse)
def create_scan(request: ScanRequest, db: Session = Depends(get_db)) -> ScanResponse:
    """
    Take the customer's order:
    1. Create a record in the Order Book (PostgreSQL)
    2. Pin the ticket on the Ticket Rack (Redis/Celery)
    3. Return the receipt number immediately
    """
    job_id = str(uuid.uuid4())

    # Write to the Order Book
    new_scan = ScanJob(id=job_id, target=request.target, status="pending")
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    # Pin the ticket — hand off to the Chefs
    process_osint_scan.delay(job_id, request.target)  # type: ignore

    return ScanResponse(job_id=new_scan.id, status=new_scan.status)


@app.get("/scans/{job_id}")
def get_scan_status(job_id: str, db: Session = Depends(get_db)) -> dict:
    """Check on an order's status."""
    scan = db.query(ScanJob).filter(ScanJob.id == job_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return {"job_id": scan.id, "target": scan.target, "status": scan.status}