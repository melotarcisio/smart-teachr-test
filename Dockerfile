FROM python:3.10

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | \
    POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Install dependencies
COPY ./ /app/
RUN poetry install --no-root

CMD [ "bash", "-c", "python -m database.migrate && poetry run python -m main" ]
