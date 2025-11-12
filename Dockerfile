FROM python:3.12-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY prototype.py /prototype.py

WORKDIR /github/workspace

RUN git config --global --add safe.directory '*'

ENTRYPOINT ["python", "/prototype.py"]