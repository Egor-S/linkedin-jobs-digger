import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class JobDescription:
    type: str
    text: str
    seniority: Optional[str] = None
    function: Optional[str] = None
    industries: Optional[str] = None


@dataclass
class JobPosting:
    id: str
    title: str
    company: str
    location: str
    date: datetime.date
    description: Optional[JobDescription] = None
