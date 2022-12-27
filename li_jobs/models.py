import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class JobDescription:
    seniority: str
    type: str
    function: str
    industries: str
    text: str


@dataclass
class JobPosting:
    id: str
    title: str
    company: str
    location: str
    date: datetime.date
    description: Optional[JobDescription] = None
