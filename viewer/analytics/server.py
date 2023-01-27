from typing import List
from functools import lru_cache

from fastapi import FastAPI
from starlette.responses import FileResponse

from .db import JobsDB
from .text import TextAnalyzer


app = FastAPI()
db = JobsDB("jobs.sqlite", text_analyzer=TextAnalyzer(
    keywords=['python', 'flask', 'fastapi', 'sqlalchemy', 'pytorch', 'numpy', 'scipy'],
    lang='en', remove_html=True
))


@app.get('/api/jobs')
@lru_cache()  # todo remove
def list_jobs() -> List[dict]:
    cur = db.c.execute(
        "SELECT jobs.id, title, company, seniority, date(date), location"
        "  FROM descriptions JOIN jobs ON jobs.id=descriptions.id"
        "  WHERE CONTAINS_LANG(text) AND CONTAINS_KEYWORDS(TEXT)"
    )
    return [
        dict(zip(['id', 'title', 'company', 'seniority', 'date', 'location'], row))
        for row in cur.fetchall()
    ]


@app.get('/api/jobs/{job_id}')
def get_job(job_id: str) -> dict:
    cur = db.c.execute(
        "SELECT jobs.id, title, company, seniority, date(date), location, text"
        "  FROM descriptions JOIN jobs ON jobs.id=descriptions.id"
        "  WHERE jobs.id=?", (job_id,)
    )
    return dict(zip(
        ['id', 'title', 'company', 'seniority', 'date', 'location', 'text'],
        cur.fetchone()
    ))


@app.get('/')
def index():
    return FileResponse("analytics/index.html")
