import datetime
from typing import Optional

from pydantic import BaseModel


class JobShort(BaseModel):
    id: str
    title: str
    company: str
    location: str
    date: datetime.date
    first_seen: datetime.datetime
    last_seen: datetime.datetime

    class Config:
        orm_mode = True


class Description(BaseModel):
    text: str
    type: str
    seniority: Optional[str] = None

    class Config:
        orm_mode = True


class JobFull(JobShort):
    description: Optional[Description] = None
