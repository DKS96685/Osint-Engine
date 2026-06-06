from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
from src.database import Base


class ScanJob(Base):
    __tablename__ = "scan_jobs"

    id = Column(String, primary_key=True, index=True)
    target = Column(String, index=True)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))