import datetime
from dataclasses import dataclass


@dataclass
class JobPosting:
    id: str
    title: str
    company: str
    location: str
    date: datetime.date
