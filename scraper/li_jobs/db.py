import sqlite3
import dataclasses
from typing import Union, List, Optional
from pathlib import Path

from .models import JobPosting, JobDescription


class JobsDB:
    def __init__(self, path: Union[Path, str]):
        self.c = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)

    def create_tables(self):
        with self.c as con:
            con.execute(
                "CREATE TABLE IF NOT EXISTS jobs"
                "(id TEXT PRIMARY KEY, title TEXT, company TEXT, location TEXT, date TIMESTAMP)"
            )
            con.execute(
                "CREATE TABLE IF NOT EXISTS descriptions"
                "(id TEXT PRIMARY KEY, type TEXT, text TEXT, seniority TEXT, function TEXT, industries TEXT)"
            )

    def insert_jobs(self, jobs: List[JobPosting]):
        with self.c as con:
            con.executemany(
                "INSERT OR IGNORE INTO jobs (id, title, company, location, date)"
                "VALUES (:id, :title, :company, :location, :date)", [dataclasses.asdict(job) for job in jobs]
            )

    def insert_description(self, job_id: str, description: JobDescription):
        with self.c as con:
            d = dataclasses.asdict(description)
            d.update({'id': job_id})
            con.execute(
                "INSERT OR IGNORE INTO descriptions (id, type, text, seniority, function, industries)"
                "VALUES (:id, :type, :text, :seniority, :function, :industries)", d
            )

    def get_description(self, job_id: str) -> Optional[JobDescription]:
        with self.c as con:
            cur = con.execute("SELECT type, text, seniority, function, industries FROM descriptions WHERE id=?", (job_id,))
            r = cur.fetchone()
        if r is None:
            return None
        return JobDescription(*r)
