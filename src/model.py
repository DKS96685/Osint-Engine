from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.database import Base

class ScanJob(Base):
    __tablename__ = "scan_jobs"

    id = Column(String, primary_key=True, index=True)
    target = Column(String, index=True)
    status = Column(String, default="pending")  # queued, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)