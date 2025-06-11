FROM python:3.12

RUN apt-get update && apt-get install -y curl

RUN mkdir /FastAPI-product-and-category

ENV POETRY_VERSION=1.8.0
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /FastAPI-product-and-category

COPY pyproject.toml poetry.lock* /FastAPI-product-and-category/

RUN poetry install --no-root

COPY . /FastAPI-product-and-category

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]