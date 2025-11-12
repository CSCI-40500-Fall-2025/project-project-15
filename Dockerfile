FROM python:3.11-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install openai gitpython requests
COPY main.py /main.py
CMD ["python", "/prototype.py"]