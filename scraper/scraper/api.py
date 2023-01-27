import logging
from enum import Enum
from typing import Optional, List, Iterator

import requests

from .parser import LinkedInJobsParser
from .db import JobCard, JobDescription
from .barrier import FrequencyBarrier


class ExperienceLevel(Enum):
    Internship = 1
    Entry = 2
    Associate = 3
    MidSenior = 4
    Director = 5


class WorkType(Enum):
    OnSite = 1
    Remote = 2
    Hybrid = 3


class LinkedInJobsAPI:
    def __init__(
            self, endpoint: str = 'https://www.linkedin.com',
            parser: Optional[LinkedInJobsParser] = None,
            logger: Optional[logging.Logger] = None,
            rpm_limit: Optional[int] = None,
            min_delay: float = 0.0
    ):
        self.s = requests.session()
        self.endpoint = endpoint.rstrip('/')
        self.parser = parser if parser is not None else LinkedInJobsParser()
        self.logger = logger if logger is not None else logging.getLogger(__name__)
        self.barrier = FrequencyBarrier(rpm_limit, min_delay)

    def _request(self, method: str, *args, **kwargs) -> requests.Response:
        self.barrier.wait()
        r = self.s.request(method, *args, **kwargs)
        self.logger.info(f"{r.status_code} - {r.url} - {r.elapsed.microseconds // 1000}ms")
        return r

    def get_url(self, path: str) -> str:
        return f"{self.endpoint}/{path.lstrip('/')}"

    def get_job_postings(
            self, keywords: str, location: str,
            age: Optional[int] = None,
            experience: Optional[List[ExperienceLevel]] = None,
            work_type: Optional[List[WorkType]] = None,
            start: int = 0
    ) -> List[JobCard]:
        url = self.get_url("/jobs-guest/jobs/api/seeMoreJobPostings/search")
        params = {'keywords': keywords, 'location': location, 'start': start}
        if age is not None:
            params['f_TPR'] = f"r{age}"
        if experience is not None:
            params['f_E'] = ','.join(str(i.value) for i in experience)
        if work_type is not None:
            params['f_WT'] = ','.join(str(i.value) for i in work_type)
        r = self._request('GET', url, params=params)
        return self.parser.get_job_postings(r.text)

    def get_job_description(self, job_id: str) -> JobDescription:
        url = self.get_url(f"/jobs-guest/jobs/api/jobPosting/{job_id}")
        r = self._request('GET', url)
        r.raise_for_status()
        return self.parser.get_job_description(r.text)

    def iter_all_job_postings(
            self, keywords: str, location: str,
            age: Optional[int] = None,
            experience: Optional[List[ExperienceLevel]] = None,
            work_type: Optional[List[WorkType]] = None,
            limit: int = 1000
    ) -> Iterator[JobCard]:
        batch_size = 25
        start = 0
        while start < limit:
            batch = self.get_job_postings(
                keywords, location, start=start,
                age=age, experience=experience, work_type=work_type
            )
            for job in batch:
                yield job
            start += len(batch)
            if len(batch) < batch_size:
                break
