FROM python:3.12-slim

# Install git (required for GitPython)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy the script
COPY prototype.py /prototype.py

# Set working directory
WORKDIR /github/workspace

# Run the script
ENTRYPOINT ["python", "/prototype.py"]