import re
import datetime
from functools import wraps
from pathlib import Path
from typing import Union, List

import bs4
import htmlmin

from .models import JobPosting, JobDescription


re_job_url_id = re.compile(r"-(\d+)\?")
criteria_names = {
    "Seniority level": 'seniority',
    "Employment type": 'type',
    "Job function": 'function',
    "Industries": 'industries'
}


def cache_data(fn):
    @wraps(fn)
    def wrapper(self, data: str, *args, **kwargs):
        if self.cache_dir:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath: Path = Path(self.cache_dir) / 'raw' / f"{timestamp}-{fn.__name__}.txt"
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with filepath.open('w') as f:
                f.write(data)
        return fn(self, data, *args, **kwargs)
    return wrapper


class LinkedInJobsParser:
    def __init__(self, cache_dir: Union[Path, str, None] = None):
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
            fields = {
                'title': self._node_text(card, 'h3.base-search-card__title'),
                'location': self._node_text(card, 'span.job-search-card__location'),
                'date': datetime.date.fromisoformat(card.find('time')['datetime'])
            }
            if card.select_one('a.base-card__full-link') is None:  # private company card
                job = JobPosting(
                    id=re_job_url_id.search(card.select_one('a.base-card--link')['href']).group(1),
                    company=self._node_text(card, 'h4.base-search-card__subtitle'),
                    **fields
                )
            else:  # normal card
                job = JobPosting(
                    id=re_job_url_id.search(card.select_one('a.base-card__full-link')['href']).group(1),
                    company=self._node_text(card, 'h4.base-search-card__subtitle > a'),
                    **fields
                )
            jobs.append(job)
        return jobs

    @cache_data
    def get_job_description(self, data: str) -> JobDescription:
        soup = bs4.BeautifulSoup(data, 'html.parser')
        criteria = {}
        item: bs4.Tag
        for item in soup.select('li.description__job-criteria-item'):
            key = self._node_text(item, 'h3.description__job-criteria-subheader')
            value = self._node_text(item, 'span.description__job-criteria-text')
            criteria[criteria_names.get(key, key)] = value
        text = htmlmin.minify(
            soup.select_one('div.description__text div.show-more-less-html__markup').prettify(),
            remove_empty_space=True
        )
        description = JobDescription(**criteria, text=text)
        return description
