import re
import datetime
from functools import wraps
from pathlib import Path
from typing import Optional, List

import bs4

from .models import JobPosting


re_job_url_id = re.compile(r"-(\d+)\?")


def cache_data(fn):
    @wraps(fn)
    def wrapper(self, data: str, *args, **kwargs):
        if self.cache_dir:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath: Path = self.cache_dir / 'raw' / f"{timestamp}-{fn.__name__}.txt"
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with filepath.open('w') as f:
                f.write(data)
        return fn(self, data, *args, **kwargs)
    return wrapper


class LinkedInJobsParser:
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir

    @staticmethod
    def _node_text(node: bs4.Tag, query: str) -> str:
        return node.select_one(query).getText().strip()

    @cache_data
    def get_job_postings(self, data: str) -> List[JobPosting]:
        soup = bs4.BeautifulSoup(data, 'html.parser')
        jobs = []
        card: bs4.Tag
        for card in soup.find_all('li'):
            job = JobPosting(
                id=re_job_url_id.search(card.select_one('a.base-card__full-link')['href']).group(1),
                title=self._node_text(card, 'h3.base-search-card__title'),
                company=self._node_text(card, 'h4.base-search-card__subtitle > a'),
                location=self._node_text(card, 'span.job-search-card__location'),
                date=datetime.date.fromisoformat(card.find('time')['datetime'])
            )
            jobs.append(job)
        return jobs
