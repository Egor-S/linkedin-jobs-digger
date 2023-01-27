from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import JobCard, JobDescription


def list_jobs(db: Session):  # -> List[JobCard]:
    return db.scalars(
        select(JobCard).join(JobDescription).filter(JobDescription.lang == 'en')
    ).all()


def get_job(db: Session, job_id: str) -> Optional[JobCard]:
    return db.get(JobCard, job_id)
