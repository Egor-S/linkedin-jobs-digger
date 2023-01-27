# LinkedIn Jobs Digger

* No login required

## Running digger

To collect Entry level Python jobs in Berlin for the last 24 hours:
```
python -m scraper.cli python@berlin --age 86400 --experience-level Entry 
```

Job postings and their full texts will be put in the SQLite database file.

## WIP

* [x] Multiple searches
* [x] Job link and brief info
* [ ] Smart post-filtering
* [x] Analyze full job description
* [x] Visualize results
