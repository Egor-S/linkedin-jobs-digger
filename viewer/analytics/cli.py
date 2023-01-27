from .db import JobsDB
from .text import TextAnalyzer


def main():
    db = JobsDB("jobs.sqlite", text_analyzer=TextAnalyzer(
        keywords=['python', 'flask', 'fastapi', 'sqlalchemy', 'pytorch', 'numpy', 'scipy'],
        lang='en', remove_html=True
    ))
    cur = db.c.execute(
        "SELECT jobs.id, title, company, seniority, location, date(date)"
        "  FROM descriptions JOIN jobs ON jobs.id=descriptions.id"
        "  WHERE CONTAINS_LANG(text) AND CONTAINS_KEYWORDS(TEXT)"
        "  ORDER BY date, location"
    )
    for row in cur.fetchall():
        print(row)


if __name__ == '__main__':
    main()
