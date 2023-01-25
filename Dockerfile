FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY li_jobs li_jobs

ENTRYPOINT ["python", "-m", "li_jobs.digger"]
