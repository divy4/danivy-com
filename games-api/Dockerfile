FROM registry-1.docker.io/library/python:3.14.7-slim

COPY games-api/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt

COPY games-api/src /app
WORKDIR /app

CMD ["python", "-m", "fastapi", "run"]
