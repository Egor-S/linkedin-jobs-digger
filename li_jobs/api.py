from typing import Optional, List

import requests

from .parser import LinkedInJobsParser
from .models import JobPosting


class LinkedInJobsAPI:
    def __init__(self, endpoint: str = 'https://www.linkedin.com', parser: Optional[LinkedInJobsParser] = None):
        self.s = requests.session()
        self.endpoint = endpoint.rstrip('/')
        self.parser = parser if parser is not None else LinkedInJobsParser()

    def get_url(self, path: str) -> str:
        return f"{self.endpoint}/{path.lstrip('/')}"

    def get_job_postings(
            self, keywords: str, location: str, age: Optional[int] = None, start: int = 0
    ) -> List[JobPosting]:
        url = self.get_url("/jobs-guest/jobs/api/seeMoreJobPostings/search")
        params = {'keywords': keywords, 'location': location, 'start': start}
        if age is not None:
            params['f_TPR'] = f"r{age}"
        r = self.s.get(url, params=params)
        return self.parser.get_job_postings(r.text)
