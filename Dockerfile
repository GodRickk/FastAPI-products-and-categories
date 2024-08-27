FROM python:3.12

RUN mkdir /fastapi_app

ENV POETRY_VERSION=1.8.0
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /fastapi_app

COPY pyproject.toml poetry.lock* /fastapi_app/

RUN poetry install --no-root --no-dev

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
