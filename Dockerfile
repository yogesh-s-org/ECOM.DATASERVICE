FROM python:3.11-slim

# Install netcat and dependencies
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Prevent Python from writing pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY utility/ .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
