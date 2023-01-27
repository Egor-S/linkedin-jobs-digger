import sys
import logging
import datetime
import argparse
from enum import EnumMeta

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .db import Base, JobCard
from .api import LinkedInJobsAPI, ExperienceLevel, WorkType
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


def resolve_enum(args: argparse.Namespace, arg_name: str, enum: EnumMeta):
    if getattr(args, arg_name) is None:
        return
    setattr(args, arg_name, [enum[i] for i in getattr(args, arg_name)])


class SearchQuery:
    def __init__(self, s: str):
        self.keywords, self.location = s.rsplit('@', maxsplit=1)

    def __repr__(self):
        return f"{self.keywords} @ {self.location}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='+', type=SearchQuery)
    parser.add_argument('--db-uri', default="sqlite:///jobs.sqlite")
    parser.add_argument('--log', default="scraper.log")
    parser.add_argument('--rpm-limit', default=10, type=int)
    parser.add_argument('--min-delay', default=3, type=float)
    parser.add_argument('--age', default=None, type=int)
    parser.add_argument('--experience-level', nargs='*', choices=[i.name for i in ExperienceLevel])
    parser.add_argument('--work-type', nargs='*', choices=[i.name for i in WorkType])
    parser.add_argument('--scan-only', action='store_true')
    parser.add_argument('--cache-dir', default=None)
    args = parser.parse_args()
    resolve_enum(args, 'experience_level', ExperienceLevel)
    resolve_enum(args, 'work_type', WorkType)

    logger = build_logger(args.log)
    logger.info(args)

    li_parser = LinkedInJobsParser(args.cache_dir)
    api = LinkedInJobsAPI(parser=li_parser, logger=logger, rpm_limit=args.rpm_limit, min_delay=args.min_delay)

    engine = create_engine(args.db_uri)
    Session = sessionmaker(engine)
    Base.metadata.create_all(bind=engine)

    found_jobs = 0
    job_ids = []
    # scan
    for query in args.query:
        for job in api.iter_all_job_postings(
            query.keywords, query.location, age=args.age,
            experience=args.experience_level, work_type=args.work_type
        ):
            with Session() as session:
                if q := session.get(JobCard, job.id):
                    job = q
                    job.last_seen = datetime.datetime.utcnow()
                else:
                    session.add(job)
                found_jobs += 1
                if job.description is None:
                    job_ids.append(job.id)
                session.commit()
    logger.info(f"Found {found_jobs} jobs")

    # fetch descriptions
    if not args.scan_only:
        logger.info(f"Fetching descriptions for {len(job_ids)} jobs")
        for job_id in job_ids:
            with Session() as session:
                job = session.get(JobCard, job_id)
                if job.description is None:
                    try:
                        job.description = api.get_job_description(job.id)
                        session.add(job)
                        session.commit()
                    except requests.HTTPError:
                        pass


if __name__ == '__main__':
    main()
