FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY viewer viewer

ENTRYPOINT ["uvicorn", "viewer.main:app"]
CMD ["--host", "0.0.0.0"]
EXPOSE 8000
