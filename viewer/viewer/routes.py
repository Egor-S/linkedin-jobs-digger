from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from . import crud
from .main import app
from .schemas import JobShort, JobFull
from .config import MODULE_ROOT
from .dependencies import get_db


@app.get('/api/jobs')
def list_jobs(db: Session = Depends(get_db)) -> List[JobShort]:
    return crud.list_jobs(db)


@app.get('/api/jobs/{job_id}')
def get_job(job_id: str, db: Session = Depends(get_db)) -> JobFull:
    return crud.get_job(db, job_id)


@app.get('/')
def index():
    return FileResponse(MODULE_ROOT / 'static' / 'index.html')
