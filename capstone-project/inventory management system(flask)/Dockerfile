# syntax=docker/dockerfile:1
FROM python

WORKDIR /our_app

# Keeps Python from generating .pyc files in the container
# Turns off buffering for easier container logging
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
gcc \
default-libmysqlclient-dev \
build-essential


COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 5000

# # Creates a non-root user with an explicit UID and adds permission to access the /app folder
# # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python3", "run.py"]
