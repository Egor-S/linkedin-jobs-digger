import sys
import logging
import argparse


from .db import JobsDB
from .api import LinkedInJobsAPI
from .parser import LinkedInJobsParser


def build_logger(path: str) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # stdout logging
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # file logging
    handler = logging.FileHandler(path, 'a')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class SearchQuery:
    def __init__(self, s: str):
        self.keywords, self.location = s.rsplit('@', maxsplit=1)

    def __repr__(self):
        return f"{self.keywords} @ {self.location}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='+', type=SearchQuery)
    parser.add_argument('--db', default="jobs.sqlite")
    parser.add_argument('--log', default="digger.log")
    parser.add_argument('--rpm-limit', default=10, type=int)
    parser.add_argument('--min-delay', default=3, type=float)
    parser.add_argument('--age', default=24 * 3600, type=int)
    parser.add_argument('--scan-only', action='store_true')
    parser.add_argument('--cache-dir', default=None)
    args = parser.parse_args()

    logger = build_logger(args.log)
    li_parser = LinkedInJobsParser(args.cache_dir)
    api = LinkedInJobsAPI(parser=li_parser, logger=logger, rpm_limit=args.rpm_limit, min_delay=args.min_delay)
    db = JobsDB(args.db)
    db.create_tables()

    jobs = []
    # scan
    for query in args.query:
        for job in api.iter_all_job_postings(query.keywords, query.location, age=args.age):
            jobs.append(job)
            db.insert_jobs([job])
    logger.info(f"Found {len(jobs)} jobs")
    # fetch descriptions
    if not args.scan_only:
        for job in jobs:
            if db.get_description(job.id) is None:
                # could fail if the job posting got unlisted :|
                db.insert_description(job.id, api.get_job_description(job.id))


if __name__ == '__main__':
    main()
