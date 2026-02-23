FROM python:3.12-slim

WORKDIR /app

# system deps (optional but common)
RUN pip install --no-cache-dir poetry

# copy only dependency files first (better caching)
COPY pyproject.toml poetry.lock* /app/

# poetry config: no venv inside container
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --only main

# copy app
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
