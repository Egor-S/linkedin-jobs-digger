from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import JobCard, JobDescription
from .dependencies import QueryParams


def list_jobs(query: QueryParams, db: Session):  # -> List[JobCard]:
    filters = [JobDescription.lang == 'en', JobDescription.contains_keywords(['python'])]
    if query.date_from is not None:
        filters.append(JobCard.date >= query.date_from)
    if query.date_till is not None:
        filters.append(JobCard.date <= query.date_till)

    return db.scalars(select(JobCard).join(JobDescription).filter(*filters)).all()


def get_job(db: Session, job_id: str) -> Optional[JobCard]:
    return db.get(JobCard, job_id)
