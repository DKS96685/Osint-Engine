from pydantic import BaseModel

# What the API expects to receive from the user
class ScanRequest(BaseModel):
    target: str
    scan_type: str = "full"

# What the API will return back to the user
class ScanResponse(BaseModel):
    job_id: str
    status: str