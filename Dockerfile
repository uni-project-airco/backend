FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

COPY app ./app

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "run:app", "--workers", "4"]
