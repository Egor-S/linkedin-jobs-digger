import logging
from typing import Optional, List

import requests

from .parser import LinkedInJobsParser
from .models import JobPosting, JobDescription
from .barrier import FrequencyBarrier


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
            self, keywords: str, location: str, age: Optional[int] = None, start: int = 0
    ) -> List[JobPosting]:
        url = self.get_url("/jobs-guest/jobs/api/seeMoreJobPostings/search")
        params = {'keywords': keywords, 'location': location, 'start': start}
        if age is not None:
            params['f_TPR'] = f"r{age}"
        r = self._request('GET', url, params=params)
        return self.parser.get_job_postings(r.text)

    def get_job_description(self, job_id: str) -> JobDescription:
        url = self.get_url(f"/jobs-guest/jobs/api/jobPosting/{job_id}")
        r = self._request('GET', url)
        return self.parser.get_job_description(r.text)
