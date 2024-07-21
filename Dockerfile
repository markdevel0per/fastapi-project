FROM python:3.12

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y redis-server
RUN pip install -r reqs.txt

CMD ["sh", "-c", "redis-server --daemonize yes && uvicorn main:app --reload --host 0.0.0.0 --port 80"]
