# base image with python
FROM python:3.11.4

WORKDIR /app
ENV IS_DOCKER=docker

RUN chmod 755 .

# Install required packages: curl, cron, postgresql-client
RUN apt-get update && \
    apt-get install -y curl cron postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install "poetry==1.6.1"

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN poetry

COPY . .

CMD ["python", "app/main.py"]
